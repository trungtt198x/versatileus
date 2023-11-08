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
    """Get DefiLlama TVL data"""
    defillama_url = "https://api.llama.fi/v2/chains"
    headers = {"accept": "*/*"}
    shimmer_tvl = None
    tvl_entries = []

    try:
        tvl_response = requests.get(defillama_url, headers=headers, timeout=10)
        tvl_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("DefiLlama TVL response: %s", tvl_response.text)
        if tvl_response.status_code == 200:
            # Extract and parse the JSON response
            tvl_data = tvl_response.json()

            # Iterate through entries and collect TVL values
            for entry in tvl_data:
                # gecko_id = entry.get("gecko_id")
                name = entry.get("name")
                tvl = entry.get("tvl")
                if name and tvl:
                    tvl_entries.append({"name": name, "tvl": tvl})

            # Sort the entries based on TVL values
            tvl_entries.sort(key=lambda x: x["tvl"], reverse=True)
            # Sort the list of dictionaries based on 'tvl' values in descending order
            sorted_data = sorted(tvl_entries, key=lambda x: x['tvl'], reverse=True)

            # Extract gecko_ids from the sorted list
            sorted_gecko_ids = [entry['name'] for entry in sorted_data]

            logger.debug(sorted_gecko_ids)

            # Find the rank of "shimmer" TVL
            for index, entry in enumerate(tvl_entries, start=1):
                if entry["name"] == "ShimmerEVM":
                    shimmer_tvl = entry["tvl"]
                    rank = index
                    break

            if shimmer_tvl is not None:
                logger.debug("Shimmer TVL Value: %s", shimmer_tvl)
                logger.debug("Shimmer TVL Rank: %s", rank)
                return {"shimmer_tvl":  shimmer_tvl, "shimmer_rank": rank}
            else:
                logger.debug("Shimmer TVL Value not found in the response.")

        # Extract and sum the respective USD converted volumes for USD and USDT
    except requests.exceptions.Timeout:
        logger.error("DefiLlama API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)