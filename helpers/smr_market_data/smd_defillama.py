""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for Shimmer from DefiLlama API
Version: 5.5.0
"""
import requests
import logging
import helpers.configuration_manager as configuration_manager

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')

async def get_defillama_data():
    """
    Get DefiLlama TVL data for ShimmerEVM.
    
    Returns:
        dict: Dictionary containing ShimmerEVM TVL and rank.
    """
    logger.info("Getting the DefiLlama TVL and rank")
    defillama_url = "https://api.llama.fi/v2/chains"
    headers = {"accept": "*/*"}
    shimmer_tvl = None
    rank = None

    try:
        tvl_response = requests.get(defillama_url, headers=headers, timeout=10)
        tvl_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("DefiLlama TVL response: %s", tvl_response.text)
        
        if tvl_response.status_code == 200:
            tvl_data = tvl_response.json()
            shimmer_entry = next((entry for entry in tvl_data if entry.get("name") == "ShimmerEVM"), None)
            
            if shimmer_entry:
                shimmer_tvl = shimmer_entry.get("tvl")
                tvl_data.sort(key=lambda x: x.get("tvl", 0), reverse=True)
                rank = tvl_data.index(shimmer_entry) + 1

                logger.debug("Shimmer TVL Value: %s", shimmer_tvl)
                logger.debug("Shimmer TVL Rank: %s", rank)
                
        return {"shimmer_tvl": shimmer_tvl, "shimmer_rank": rank}

    except requests.exceptions.Timeout:
        logger.error("DefiLlama API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)