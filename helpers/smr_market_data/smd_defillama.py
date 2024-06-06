""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for IOTA from DefiLlama API
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
    Get DefiLlama TVL data for IOTA EVM.
    
    Returns:
        dict: Dictionary containing IOTA EVM TVL and rank.
    """
    logger.info("Getting the DefiLlama TVL and rank")
    defillama_url = "https://api.llama.fi/v2/chains"
    headers = {"accept": "*/*"}
    iota_tvl = None
    rank = None

    try:
        tvl_response = requests.get(defillama_url, headers=headers, timeout=10)
        tvl_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("DefiLlama TVL response: %s", tvl_response.text)
        
        if tvl_response.status_code == 200:
            tvl_data = tvl_response.json()
            iota_entry = next((entry for entry in tvl_data if entry.get("name") == "IOTA EVM"), None)
            
            if iota_entry:
                iota_tvl = iota_entry.get("tvl")
                tvl_data.sort(key=lambda x: x.get("tvl", 0), reverse=True)
                rank = tvl_data.index(iota_entry) + 1

                logger.debug("IOTA TVL Value: %s", iota_tvl)
                logger.debug("IOTA TVL Rank: %s", rank)
                
        return {"iota_tvl": iota_tvl, "iota_rank": rank}

    except requests.exceptions.Timeout:
        logger.error("DefiLlama API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)