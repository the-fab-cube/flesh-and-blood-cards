import { fetchGroupProductDetails } from './fetch-group-product-details.js'

const extractBearerTokenFromArgs = () => {
    const bearer = process.argv[3]

    if (!bearer) {
        console.error('ERROR: Expected a bearer token as 2nd argument!');
        process.exit(1);
    }

    return bearer
}

const extractGroupIdFromArgs = () => {
    const bearer = process.argv[2]

    if (!bearer) {
        console.error('ERROR: Expected a TCGPlayer groupId as 1st argument!');
        process.exit(1);
    }

    return bearer
}

const bearerToken = extractBearerTokenFromArgs()
const groupId = extractGroupIdFromArgs()

await fetchGroupProductDetails(groupId, bearerToken)