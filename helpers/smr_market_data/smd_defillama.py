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

# swirl, pools-finance, virtue
protocols = config["protocols"]

async def get_defillama_data():
    """
    Get DefiLlama TVL data for both IOTA EVM and IOTA L1 and also calc rank.
    
    Returns:
        dict: Dictionary containing IOTA EVM TVL and rank.
    """
    logger.info("Getting the DefiLlama TVL and rank")
    defillama_url = "https://api.llama.fi/v2/chains"
    headers = {"accept": "*/*"}
    iota_evm_tvl = None
    iota_evm_rank = None
    iota_L1_tvl = None
    iota_L1_rank = None

    try:
        tvl_response = requests.get(defillama_url, headers=headers, timeout=10)
        tvl_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("DefiLlama TVL response: %s", tvl_response.text)
        
        if tvl_response.status_code == 200:
            tvl_data = tvl_response.json()
            # iota_entry = next((entry for entry in tvl_data if entry.get("name") == "IOTA EVM"), None)

            targets = {"IOTA EVM", "IOTA"}
            matched_entries = [entry for entry in tvl_data if entry.get("name") in targets]

            # Optionally unpack them if you're sure both exist
            iota_evm_entry = next((e for e in matched_entries if e.get("name") == "IOTA EVM"), None)
            iota_L1_entry = next((e for e in matched_entries if e.get("name") == "IOTA"), None)

            tvl_data.sort(key=lambda x: x.get("tvl", 0), reverse=True)
            
            if iota_evm_entry:
                iota_evm_tvl = iota_evm_entry.get("tvl")
                iota_evm_rank = tvl_data.index(iota_evm_entry) + 1
                logger.debug("iota_evm_tvl: %s", iota_evm_tvl)
                logger.debug("iota_evm_rank: %s", iota_evm_rank)

            if iota_L1_entry:
                iota_L1_tvl = iota_L1_entry.get("tvl")
                iota_L1_rank = tvl_data.index(iota_L1_entry) + 1
                logger.debug("iota_L1_tvl: %s", iota_L1_tvl)
                logger.debug("iota_L1_rank: %s", iota_L1_rank)

        return {"iota_evm_tvl": iota_evm_tvl, "iota_evm_rank": iota_evm_rank, "iota_L1_tvl": iota_L1_tvl, "iota_L1_rank": iota_L1_rank}

    except requests.exceptions.Timeout:
        logger.error("DefiLlama API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)

async def get_tvl_protocols():
    """
    Get DefiLlama TVL for protocols on IOTA L1
    """
    logger.info("Get DefiLlama TVL for protocols on IOTA L1")
    defillama_url = "https://api.llama.fi/tvl"
    headers = {"accept": "*/*"}

    tvl_protocols = {}

    for protocol in protocols:
        try:
            tvl_response = requests.get(f"{defillama_url}/{protocol}", headers=headers, timeout=10)
            tvl_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
            logger.debug("DefiLlama TVL response: %s", tvl_response.text)
            
            if tvl_response.status_code == 200:
                tvl_data = tvl_response.json()
                tvl_protocols[protocol] = tvl_data

        except requests.exceptions.RequestException:
            tvl_protocols[protocol] = 0
            logger.error("DefiLlama API RequestException.")

    return tvl_protocols
