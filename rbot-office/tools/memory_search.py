import os
import requests

def search_rag(query: str, workspace_slug: str) -> str:
	"""Queries the AnythingLLM vector database for relevant information."""
	api_key = os.getenv("ANYTHINGLLM_API_KEY")
	base_url = "http://localhost:3001/api/v1"
	
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}

	try:
		# Query the specific workspace
		payload = {
			"message": query,
			"mode": "chat"
		}
		
		url = f"{base_url}/workspace/{workspace_slug}/chat"
		res = requests.post(url, headers=headers, json=payload)
		res.raise_for_status()
		
		data = res.json()
		text_response = data.get("textResponse", "")
		
		# Extract source filenames so the AI knows where the info came from
		sources = data.get("sources", [])
		source_names = list(set([src.get("title", "Unknown Document") for src in sources]))
		
		if not text_response:
			return "No relevant information found in the database."
			
		return f"Database Response: {text_response}\n\nSources Found: {', '.join(source_names)}"

	except Exception as e:
		return f"Failed to search RAG: {str(e)}"
