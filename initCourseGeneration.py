from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.vectorstores.utils import DistanceStrategy
from langchain_google_community import BigQueryVectorSearch
from langchain_community.document_loaders import NewsURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import json
import google.generativeai as genai
import numpy as np
from common import ex_output, safe, config, topic_json_format, stem_topics


class InitCourseRecommendation:
    def __init__(self, request, project_id, dataset_name, table_name, location):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.request = request
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
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

    def generate_recommendation(self):
        prompt = f"Based on the user interested topic in {self.request['interestTopic']}, decide recommended 5 course topic in total that related to it. Return in JSON format: {topic_json_format}. Do not write 'json' or 'JSON' on it."

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
              "correct_answer": "Only One correct answer"
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
          - Each explanation should include the following sections (limited to 50 words each):
              Title: Short and descriptive.
              Topic: The general category from the provided list `{stem_topics}` (avoid subtopics).
              Description (Overview):** A brief introduction to the topic.
              Detail Explanation (Main Material):** The core information about the topic.
              Multiple Choice Quiz:** 
                  One question with 3 answer choices
                  IMPORTANT: Only One correct answer
              Summary: A concise recap of the key points.
           - Target Audience: Age {self.request['age']}. Content language must be appropriate for this age group!
           - Source: `{sources}` (citation information for the content).

          Output Format:
          start with [ and end with ]. Do not write json, JSON or ```.

          Structured JSON array following this format: {json_format}

          Example Output: {ex_output}

        """

        response = self.model.generate_content(
            prompt, safety_settings=safe, generation_config=config

        )

        rec = response.text
        print(rec)
        rec_out = rec.replace('\n', '').replace('json', '').replace('```', '').replace('  ', '').replace('\\', '').replace('\'', '').replace("'", '"').replace('JSON', '')
        rec_json = json.loads(rec_out)

        return rec_json