import axios from 'axios'

export const fetchGroupProductDetails = async (groupId, bearerToken) => {
    const productIds = await fetchAllGroupProductIds(groupId, bearerToken)
    const productDetails = await fetchAllGroupProductDetails(productIds, bearerToken)

    return productDetails
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
        const startIndex = offset
        let endIndex = offset + limit

        if (endIndex >= productIds.length) {
            endIndex = productIds.length
        }


        const productIdSubsection = productIds.slice(startIndex, endIndex)

        let response = await makeGetProductDetailsCall(productIdSubsection, bearerToken)
        productDetails = productDetails.concat(response.results.map(result => formatProductDetail(result)))

        offset += limit
    }
    
    productDetails.forEach(splitDFCIntoTwoEntries)

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

// Object mapping //

const formatProductDetail = (productDetail) => {
    const name = productDetail.name
    const productId = productDetail.productId
    const rarity = formatRarity(productDetail.extendedData.find(dataElement => dataElement.name.toLowerCase() == 'rarity')?.value)
    const cardId = productDetail.extendedData.find(dataElement => dataElement.name.toLowerCase() == 'number')?.value

    return {
        name,
        productId,
        rarity,
        cardId
    }
}

const formatRarity = (rarity) => {
    switch (rarity?.toLowerCase()) {
        case 'token':
            return 'T'
        case 'common':
            return 'C'
        case 'rare':
            return 'R'
        case 'super rare':
            return 'S'
        case 'majestic':
            return 'M'
        case 'legendary':
            return 'L'
        case 'fable':
        case 'fabled':
            return 'F'
        case 'marvel':
            return 'V'
        case 'promo':
            return 'P'
        default:
            return rarity
    }
}

const splitDFCIntoTwoEntries = (productDetail, index, array) => {
    if (productDetail.name.includes("//") && productDetail.cardId.includes("//")) {

        const splitName = productDetail.name.split("//")
        const splitCardId = productDetail.cardId.split("//")

        if (splitName.length == 2 && splitCardId.length == 2) {
            productDetail.name = splitName[0].trim()
            productDetail.cardId = splitCardId[0].trim()

            array.push({
                name: splitName[1].trim(),
                productId: productDetail.productId,
                rarity: productDetail.rarity,
                cardId: splitCardId[1].trim()
            })
        }
    }
}