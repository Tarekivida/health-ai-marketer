import json
import sys
from litellm import completion
from utils.llm_config import local_llm_config  # Ensure correct config import

def extract(article):
    """
    Extracts products and solutions mentioned in the given article text using LiteLLM.
    Returns a JSON dictionary with relevant extracted information.
    """
    print("🔍 Extracting product and solution data from the article using LiteLLM...")
    
    try:
        response = completion(
            model=local_llm_config["config_list"][0]["model"],  # Use model from config
            messages=[
                {"role": "system", "content": "Extract products and solutions from the given text and return them as a structured JSON dictionary."},
                {"role": "user", "content": article}
            ]
        )

        extracted_data = json.loads(response["choices"][0]["message"]["content"])
        return extracted_data

    except json.JSONDecodeError:
        print("❌ Error: Failed to parse extracted data as JSON.")
        return None
    except Exception as e:
        print(f"❌ Unexpected error during extraction: {e}")
        return None

def test_product_extraction():
    article = """    
    **Dry Skin**
    
    **Introduction**
    
    Dry skin, also known as xerosis, is a common condition characterized by a lack of moisture on the skin's surface. It can affect anyone, regardless of age or skin type, but it is more prevalent in older adults and people with certain medical conditions. Dry skin can be uncomfortable, itchy, and even painful, making everyday activities challenging.
    
    **Causes**
    
    The primary causes of dry skin include:
    
    1.  **Genetics**: Some people may inherit a tendency to have dry skin due to their genetic makeup.
    2.  **Environmental factors**: Cold weather, low humidity, and exposure to harsh soaps or detergents can strip the skin of its natural moisture barrier.
    3.  **Medical conditions**: Certain health conditions, such as eczema, psoriasis, and diabetes, can increase the risk of developing dry skin.
    4.  **Medications**: Some medications, including diuretics, beta-blockers, and certain antidepressants, can cause dry skin as a side effect.
    5.  **Lifestyle habits**: Frequent bathing, using hot water, or not moisturizing regularly can contribute to dry skin.
    
    **Symptoms**
    
    The symptoms of dry skin may vary depending on the severity of the condition. Common signs include:
    
    1.  **Itching**: Dry skin can cause intense itching, especially after bathing or showering.
    2.  **Flakiness**: The skin may become flaky and rough to the touch.
    3.  **Redness**: Dry skin can lead to redness and inflammation, particularly on the hands, feet, elbows, and knees.
    4.  **Cracking**: In severe cases, dry skin can cause cracks in the skin, making it more susceptible to infection.
    
    **Treatment Options**
    
    There are various treatment options available for dry skin, including:
    
    1.  **Moisturizers**: Using a gentle moisturizer regularly can help lock in moisture and soothe dry skin.
    2.  **Topical creams**: Over-the-counter or prescription creams containing ingredients like urea, hyaluronic acid, or ceramides can provide long-lasting hydration.
    3.  **Oatmeal baths**: Oatmeal has anti-inflammatory properties that can help relieve itching and irritation.
    4.  **Humidifiers**: Using a humidifier in dry environments can add moisture to the air and alleviate dry skin symptoms.
    
    **Prevention Strategies**
    
    To prevent dry skin, follow these tips:
    """
    
    print("🔍 Running Product Extraction Test...")
    
    try:
        extracted_data = extract(article)
        
        if isinstance(extracted_data, dict):
            print("✅ Extracted Product and Solutions:")
            print(json.dumps(extracted_data, indent=4))
        else:
            print("❌ Error: Extracted data is not in dictionary format.")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔍 Running Product Extraction Test...")
    extracted_data = extract(article)
    
    if extracted_data:
        print("✅ Extracted Product and Solutions:")
        print(json.dumps(extracted_data, indent=4))
    else:
        print("❌ Error: Extraction failed.")
