import { fetchGroupProductDetails } from './fetch-group-product-details.js'
import { populateProductIds } from './populate-product-ids.js'

const extractGroupIdFromArgs = () => {
    const groupId = parseInt(process.argv[2])

    if (!groupId) {
        console.error('ERROR: Expected a TCGPlayer groupId as 1st argument!');
        process.exit(1);
    }

    return groupId
}

const extractSetIdFromArgs = () => {
    const setId = process.argv[3]

    if (!setId) {
        console.error('ERROR: Expected a TCGPlayer groupId as 2nd argument!');
        process.exit(1);
    }

    return setId
}

const extractBearerTokenFromArgs = () => {
    const bearer = process.argv[4]

    if (!bearer) {
        console.error('ERROR: Expected a bearer token as 3rd argument!');
        process.exit(1);
    }

    return bearer
}

const groupId = extractGroupIdFromArgs()
const setId = extractSetIdFromArgs()
const bearerToken = extractBearerTokenFromArgs()

const productDetails = await fetchGroupProductDetails(groupId, bearerToken)
await populateProductIds(productDetails, 'english', setId, 4, 8, 14)