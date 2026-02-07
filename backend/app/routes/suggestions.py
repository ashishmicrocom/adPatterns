from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import os

router = APIRouter()

# Load model data (CSV from notebook)
# Try multiple paths to ensure it works locally and in production
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CSV_PATH = os.path.join(BASE_DIR, "adpattern_final_production.csv")

# Fallback paths for different deployment scenarios
if not os.path.exists(CSV_PATH):
    # Try relative to backend folder
    CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "../adpattern_final_production.csv")
    CSV_PATH = os.path.abspath(CSV_PATH)

class SuggestionRequest(BaseModel):
    category: Optional[str] = "Clothing"
    user_description: Optional[str] = None
    price: Optional[str] = None
    price_range: Optional[str] = None
    gender: Optional[str] = "Male"
    age_min: Optional[int] = 1
    age_max: Optional[int] = 100
    locations: Optional[str] = None
    target_audience: Optional[str] = None
    platform: Optional[str] = "Meta"  # Platform from model: Meta, Google

class SuggestionResponse(BaseModel):
    headlines: List[str]
    descriptions: List[str]
    keywords: List[str]
    image_prompts: List[str]
    cta: str
    total_matches: int

@router.post("/generate-suggestions", response_model=SuggestionResponse)
async def generate_suggestions(request: SuggestionRequest):
    """
    Generate AI suggestions from model data based on campaign parameters.
    Filters model CSV by category, gender, age range and returns matching headlines/descriptions.
    """
    try:
        # Check if CSV exists
        if not os.path.exists(CSV_PATH):
            # Return mock data if CSV not found (for development)
            return SuggestionResponse(
                headlines=[
                    "Premium fashion crafted for everyday comfort shop today",
                    "Stylish clothing designed for modern lifestyle explore now",
                    "Elegant apparel tailored for confident look discover more"
                ],
                descriptions=[
                    "Experience premium clothing that combines style and comfort for everyday wear",
                    "Modern fashion collection designed for confident individuals",
                    "Discover elegant apparel crafted for your active lifestyle"
                ],
                keywords=["premium", "fashion", "clothing", "style", "comfort"],
                image_prompts=[
                    "Premium stylish clothing photoshoot",
                    "Modern fashion apparel lifestyle",
                    "Elegant comfortable wear collection"
                ],
                cta="Shop Now",
                total_matches=0
            )
        
        # Load model data
        df = pd.read_csv(CSV_PATH)
        
        # Filter by category
        filtered_df = df[df['Category'] == request.category]
        
        # Filter by platform (model has Platform column: Meta, Google)
        if request.platform:
            filtered_df = filtered_df[filtered_df['Platform'] == request.platform]
        
        # Filter by gender (if model has specific gender, match it; "All" in frontend maps to any gender in model)
        if request.gender and request.gender != "All":
            filtered_df = filtered_df[filtered_df['Gender'] == request.gender]
        
        # Filter by age range (model has Age_Min and Age_Max)
        if request.age_min and request.age_max:
            # Find rows where the age ranges overlap
            filtered_df = filtered_df[
                (filtered_df['Age_Min'] <= request.age_max) & 
                (filtered_df['Age_Max'] >= request.age_min)
            ]
        
        # If locations specified, try to find matching locations (model has comma-separated Locations)
        if request.locations:
            user_locations = [loc.strip().lower() for loc in request.locations.split(',')]
            # Filter rows where any location matches
            def location_matches(row_locations):
                if pd.isna(row_locations):
                    return False
                model_locations = [loc.strip().lower() for loc in str(row_locations).split(',')]
                return any(loc in model_locations for loc in user_locations)
            
            filtered_df = filtered_df[filtered_df['Locations'].apply(location_matches)]
        
        # If no matches found, use all data from same category
        if len(filtered_df) == 0:
            filtered_df = df[df['Category'] == request.category]
        
        # If still no matches, use all data
        if len(filtered_df) == 0:
            filtered_df = df
        
        # Get headlines, descriptions, keywords, and prompts (up to 10 items)
        # Don't use unique() since each product should have 10 distinct ads
        # Just limit the results to avoid too much data
        headlines = filtered_df['Headline'].dropna().head(10).tolist()
        descriptions = filtered_df['Ad_Description'].dropna().head(10).tolist()
        keywords = filtered_df['Keyword'].dropna().head(10).tolist()
        image_prompts = filtered_df['Image_Prompt'].dropna().head(10).tolist()
        
        # Determine CTA based on price
        cta = "Shop Now" if request.price or request.price_range else "Learn More"
        
        return SuggestionResponse(
            headlines=headlines,
            descriptions=descriptions,
            keywords=keywords,
            image_prompts=image_prompts,
            cta=cta,
            total_matches=len(filtered_df)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

@router.get("/model-stats")
async def get_model_stats():
    """Get statistics about the model data"""
    try:
        if not os.path.exists(CSV_PATH):
            return {"error": "Model CSV not found", "path": CSV_PATH}
        
        df = pd.read_csv(CSV_PATH)
        
        return {
            "total_rows": len(df),
            "total_users": df['User_ID'].nunique(),
            "categories": df['Category'].unique().tolist(),
            "genders": df['Gender'].unique().tolist(),
            "platforms": df['Platform'].unique().tolist(),
            "age_range": f"{df['Age_Min'].min()} - {df['Age_Max'].max()}",
            "unique_headlines": df['Headline'].nunique(),
            "unique_descriptions": df['Ad_Description'].nunique(),
            "csv_path": CSV_PATH
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
