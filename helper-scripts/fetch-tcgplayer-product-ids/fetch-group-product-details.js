import axios from 'axios'

export const fetchGroupProductDetails = async (groupId, bearerToken) => {
    const productIds = await fetchAllGroupProductIds(groupId, bearerToken)
    const productDetails = await fetchAllGroupProductDetails(productIds, bearerToken)
    console.log(productDetails)
}

const fetchAllGroupProductIds = async (groupId, bearerToken) => {
    const limit = 100 // 100 is the max limit allowed by TCGPlayer
    let offset = 0
    let initialResponse = await makeGroupProductsCall(groupId, limit, offset, bearerToken)

    let productIds = initialResponse.results.map(result => result.productId)
    let productCount = initialResponse.totalItems

    while ((offset + limit) <= productCount) {
        offset += limit

        let response = await makeGroupProductsCall(groupId, limit, offset, bearerToken)
        productIds = productIds.concat(response.results.map(result => result.productId))
    }

    return productIds
}

const fetchAllGroupProductDetails = async (productIds, bearerToken) => {
    const limit = 100
    let offset = 0
    let productDetails = []

    while (offset <= productIds.length) {
        offset += limit

        const startIndex = offset
        let endIndex = offset + limit

        if (endIndex >= productIds.length) {
            endIndex = productIds.length
        }

        const productIdSubsection = productIds.slice(startIndex, endIndex)

        let response = await makeGetProductDetailsCall(productIdSubsection, bearerToken)
        productDetails = productDetails.concat(response.results.map(result => result)) // TODO: Map to expected object
    }

    return productDetails
}

// TCGPlayer Endpoint calls

const makeGroupProductsCall = async (groupId, limit, offset, bearerToken) => {
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

const makeGetProductDetailsCall = async (productIds, bearerToken) => {
    if (productIds.length > 100) {
        throw new Error("Should not fetch more than 100 product IDs at a time from TCGPlayer endpoint")
    }

    const config = {
        params: {
            getExtendedFields: true
        },
        headers: {
            Authorization: `Bearer ${bearerToken}`
        }
    }

    const url = `https://api.tcgplayer.com/catalog/products/${productIds.join(',')}`

    return (await axios.get(url, config)).data
}