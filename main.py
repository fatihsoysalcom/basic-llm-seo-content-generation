import os
import json
import http.client

def generate_seo_content_with_claude(topic: str, keywords: list[str]) -> dict:
    """
    Generates SEO-optimized meta description and content idea using Anthropic's Claude LLM.
    This simulates a core function of the Claude-SEO architecture discussed in the article.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    conn = http.client.HTTPSConnection("api.anthropic.com")

    # Construct the prompt for the LLM to act as an SEO assistant
    prompt_content = f"""You are an expert SEO assistant. Given the following topic and keywords, generate a compelling meta description (under 160 characters) and a brief content idea for a blog post.

Topic: {topic}
Keywords: {', '.join(keywords)}

Format your response as follows:
Meta Description: [Your meta description here]
Content Idea: [Your content idea here]
"""

    payload = {
        "model": "claude-3-haiku-20240307", # Using a cost-effective Claude model for demonstration
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": prompt_content}
        ]
    }

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    try:
        conn.request("POST", "/v1/messages", json.dumps(payload), headers)
        response = conn.getresponse()
        response_data = response.read().decode("utf-8")

        if response.status != 200:
            print(f"Error: {response.status} - {response_data}")
            return {"error": f"API call failed with status {response.status}", "details": response_data}

        response_json = json.loads(response_data)
        
        # Extract the generated text from the LLM response
        generated_text = ""
        if "content" in response_json and len(response_json["content"]) > 0:
            for block in response_json["content"]:
                if block.get("type") == "text":
                    generated_text += block["text"]
        
        # Parse the structured output from the LLM's response
        meta_desc = "N/A"
        content_idea = "N/A"
        
        lines = generated_text.strip().split('\n')
        for line in lines:
            if line.startswith("Meta Description:"):
                meta_desc = line.replace("Meta Description:", "").strip()
            elif line.startswith("Content Idea:"):
                content_idea = line.replace("Content Idea:", "").strip()

        return {
            "meta_description": meta_desc,
            "content_idea": content_idea,
            "raw_response": generated_text # Include raw for debugging/completeness
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    # --- Example Usage ---
    # This demonstrates how an LLM can be used for automated SEO tasks,
    # a core concept of the Claude-SEO architecture discussed in the article.
    
    target_topic = "Yapay Zeka ile Üretim Seviyesi SEO Ajanı Mimarisi" # Article's topic
    target_keywords = ["Claude-SEO", "AI SEO", "otomasyon", "üretim seviyesi", "LLM"]

    print(f"Generating SEO content for topic: '{target_topic}' with keywords: {target_keywords}")
    print("-" * 60)

    result = generate_seo_content_with_claude(target_topic, target_keywords)

    if "error" in result:
        print(f"An error occurred: {result['error']}")
        if "details" in result:
            print(f"Details: {result['details']}")
    else:
        print(f"Generated Meta Description: {result['meta_description']}")
        print(f"Generated Content Idea: {result['content_idea']}")
    print("-" * 60)

    # Another example to showcase versatility
    target_topic_2 = "E-ticaret Siteleri İçin Anahtar Kelime Araştırması Stratejileri"
    target_keywords_2 = ["e-ticaret SEO", "anahtar kelime analizi", "ürün SEO", "rekabet analizi"]

    print(f"\nGenerating SEO content for topic: '{target_topic_2}' with keywords: {target_keywords_2}")
    print("-" * 60)
    result_2 = generate_seo_content_with_claude(target_topic_2, target_keywords_2)

    if "error" in result_2:
        print(f"An error occurred: {result_2['error']}")
        if "details" in result_2:
            print(f"Details: {result_2['details']}")
    else:
        print(f"Generated Meta Description: {result_2['meta_description']}")
        print(f"Generated Content Idea: {result_2['content_idea']}")
    print("-" * 60)
