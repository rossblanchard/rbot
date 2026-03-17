import os
import requests

def commit_to_rag(title: str, content: str, workspace_slug: str) -> str:
	"""Uploads text to AnythingLLM and embeds it into the workspace."""
	api_key = os.getenv("ANYTHINGLLM_API_KEY")
	base_url = "http://localhost:3001/api/v1"
	
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}

	try:
		# Step 1: Upload the raw text as a document
		upload_payload = {
			"textContent": content,
			"metadata": {"title": title}
		}
		upload_res = requests.post(f"{base_url}/document/raw-text", headers=headers, json=upload_payload)
		upload_res.raise_for_status()
		
		# Extract the location ID of the new document
		doc_location = upload_res.json().get("documents", [{}])[0].get("location")
		if not doc_location:
			return "Error: Document uploaded, but failed to retrieve storage location."

		# Step 2: Pin the document to the Workspace and Embed it
		empty_list =[]
		embed_payload = {
			"adds": [doc_location],
			"deletes": empty_list
		}
		
		embed_url = f"{base_url}/workspace/{workspace_slug}/update-embeddings"
		embed_res = requests.post(embed_url, headers=headers, json=embed_payload)
		embed_res.raise_for_status()

		return f"Success: Memory '{title}' has been successfully embedded into the '{workspace_slug}' RAG database."

	except Exception as e:
		return f"Failed to commit to RAG: {str(e)}"
