import * as nanoid from 'nanoid'
import nanoidDictionary from 'nanoid-dictionary';

export const customNanoId = nanoid.customAlphabet(nanoidDictionary.nolookalikesSafe)

export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}