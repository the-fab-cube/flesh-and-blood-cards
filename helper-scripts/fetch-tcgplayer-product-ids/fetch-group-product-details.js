import axios from 'axios'

export const fetchGroupProductDetails = async (groupId, bearerToken) => {
    const productIds = await fetchAllGroupProductIds(groupId, bearerToken)
}

const fetchAllGroupProductIds = async (groupId, bearerToken) => {
    const limit = 100 // 100 is the max limit allowed by TCGPlayer
    let offset = 0
    let initialResponse = await makeGroupProductDetailsCall(groupId, limit, offset, bearerToken)

    let productIds = initialResponse.results.map(result => result.productId)
    let productCount = initialResponse.totalItems

    while ((offset + limit) <= productCount) {
        offset += limit

        let response = await makeGroupProductDetailsCall(groupId, limit, offset, bearerToken)
        productIds = productIds.concat(response.results.map(result => result.productId))
    }

    return productIds
}

const makeGroupProductDetailsCall = async (groupId, limit, offset, bearerToken) => {
    const config = {
        params: {
            groupId,
            limit,
            offset
        },
        headers: {
            Authorization: `Bearer ${bearerToken}`
        }
    }

    return (await axios.get("https://api.tcgplayer.com/catalog/products", config)).data
}