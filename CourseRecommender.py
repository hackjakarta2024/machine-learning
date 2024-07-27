from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
# from langchain_community.document_loaders import WebBaseLoader
from langchain_google_vertexai import VertexAIEmbeddings
# from google.cloud import bigquery
from langchain.vectorstores.utils import DistanceStrategy
from langchain_google_community import BigQueryVectorSearch
from langchain_community.document_loaders import NewsURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import json
import google.generativeai as genai
import numpy as np
from implicit.als import AlternatingLeastSquares
from scipy.sparse import coo_matrix
import pandas_gbq as pdgbq
from common import ex_output, safe, config, topic_json_format, stem_topics


class CourseRecommendation:
    def __init__(self, request, project_id, dataset_name, table_name, location):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.request = request
        self.model = genai.GenerativeModel('gemini-1.0-pro-latest')
        self.search = GoogleSearchAPIWrapper()
        self.embedding = VertexAIEmbeddings(model_name="textembedding-gecko", project=project_id)
        self.store = BigQueryVectorSearch(
            project_id=project_id,
            dataset_name=dataset_name,
            table_name=table_name,
            location=location,
            embedding=self.embedding,
            distance_strategy=DistanceStrategy.COSINE
        )

    def top_results(self, query):
        return self.search.results(query, 3)
    
    def query_from_bq(self, project_id, region, dataset, table_name):
        query = f"""
        SELECT * FROM EXTERNAL_QUERY("{project_id}.{region}.{dataset}",
        "SELECT CAST(user_id as varchar) as user, CAST(topic_id as varchar) as topic, count_like FROM {table_name};");
        """
        df = pdgbq.read_gbq(query, project_id=project_id,  use_bqstorage_api=True)
        return df

    def als_model_training(self, df):
        user_to_idx = {user: idx for idx, user in enumerate(df['user'].unique())}
        topic_to_idx = {topic: idx for idx, topic in enumerate(df['topic'].unique())}

        df['user_idx'] = df['user'].map(user_to_idx)
        df['topic_idx'] = df['topic'].map(topic_to_idx)

        likes_matrix = coo_matrix((df['count_like'], (df['topic_idx'], df['user_idx'])))

        model = AlternatingLeastSquares(factors=50, regularization=0.01)
        model.fit(likes_matrix.T)

        return model, user_to_idx, topic_to_idx
    
    def recommend_topics(self, user_id, user_to_idx, topic_to_idx, model, N=5):
        user_idx = user_to_idx.get(user_id)
        user_preferences = model.user_factors[user_idx]
        topic_scores = model.item_factors.dot(user_preferences)
        top_topic_indices = topic_scores.argsort()[::-1][:N]
        recommended_topics = [topic for topic, idx in topic_to_idx.items() if idx in top_topic_indices]

        return recommended_topics

    def extract_sentences_from_web(self, links, chunk_size=500, chunk_overlap=30):
        data = []
        for link in links:
            loader = NewsURLLoader(urls=link)
            data += loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        sentences = text_splitter.split_documents(data)
        return sentences

    def search_and_store_topics(self, topic_json):
        links = []

        for topic in topic_json['courseTopic']:
            results = self.top_results(topic)
            link = [results[i]['link'] for i in range(len(results))]
            links.append(link)

        sentences = self.extract_sentences_from_web(links)

        data = {"sources": []}

        for document in sentences:
            source = document.metadata.get('link')
            data["sources"].append(source)

        page_content = [str(sentences[x].page_content) for x in range(len(sentences))]
        self.store.add_texts(page_content, [{"source": link} for link in data['sources']] )

    def generate_recommendation(self, df, user_id):
        model, user_to_idx, topic_to_idx = self.als_model_training(df)
        recommended_topics = self.recommend_topics(user_id, user_to_idx, topic_to_idx, model)

        print(recommended_topics)

        prompt = f"Based on the user interested topic in {recommended_topics}, decide recommended 5 course topic in total that related to it. Return in JSON format: {topic_json_format}. Do not write 'json' or 'JSON' on it."

        response = self.model.generate_content(
            prompt, safety_settings=safe, generation_config=config

        )

        topic_json = response.text
        topic_json = json.loads(topic_json.replace('\n', '').replace('json', '').replace('```', '').replace('JSON', ''))

        all_recommended_topics = []

        for topic_dict in topic_json['courseTopic']:
            for recommended_topic in topic_dict.values():
                all_recommended_topics.append(recommended_topic)
        
        query = ", ".join(all_recommended_topics)
        docs = self.store.similarity_search_with_relevance_scores(query, k=10)
        score = [doc[1] for doc in docs]
        avg_score = sum(score) / len(score)

        while avg_score < 0.5:
            self.search_and_store_topics(self, topic_json)
            docs = self.store.similarity_search_with_relevance_scores(query, k=10)
            score = [doc[1] for doc in docs]
            avg_score = sum(score) / len(score)

        page_contents = [doc[0].page_content for doc in docs]
        sources = np.unique([doc[0].metadata['source'] for doc in docs])
        context = '. '.join(page_contents)

        json_format = f"""[
          {{
            "title": "",
            "topic": "",
            "material": "",
            "description": "",
            "quiz": {{
              "question": "",
              "choices": [
                "",
                "",
                ""
              ],
              "correct_answer": ""
            }},
            "summary": "",
            "source": {sources}
          }}
        ]"""

        prompt = f"""

          Context: {context}.
          Topics: A list of topics separated by commas (`{query}`). There are a total of {len(query.split(','))} topics.

          Task:

          - Explain each topic in a clear and concise way, similar to a bite-sized course.
          - Each explanation should include the following sections (limited to 40 words each):
              Title: Short and descriptive.
              Topic: The general category from the provided list `{stem_topics}` (avoid subtopics).
              Description (Overview):** A brief introduction to the topic.
              Detail Explanation (Main Material):** The core information about the topic.
              Multiple Choice Quiz:** 
                  One question with answer choices
                  The correct answer identified
              Summary:** A concise recap of the key points.
           - Source:** `{sources}` (citation information for the content).

          Output Format:

          Structured JSON array following this format: {json_format}

          Example Output: {ex_output}

        """

        response = self.model.generate_content(
            prompt, safety_settings=safe, generation_config=config
        )

        rec = response.text
        print(rec)
        rec_out = rec.replace('\n', '').replace('json', '').replace('```', '').replace('  ', '').replace('\\', '').replace('\'', '').replace("'", '"')
        rec_json = json.loads(rec_out)

        return rec_json