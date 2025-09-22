# Problem Set 2: Composing Concepts

## Concept

1. Contexts are used to keep a list of strings that we do not want to duplicate, i.e the unique string returned should not match any string in the context. In the URL Shortening app, the context would be a list of shortUrl suffices.

2. The NonceGeneration store sets of used strings in order to generate random strings that do not duplicate any of the strings in the used set. In the case of maintaining a counter, it is related to the used strings set because they both store information about what has already been used. All integers up the the stored number has already been used, like how all strings in the set has already been used. The counter simply abstracts away all used numbers and stores only the most recently used number. However, with a counter, the next generated string is predictable, whereas with the used set, it can be more randomized.

3. Advantage: URL suffix is easy for user to remember and say, allowing for easier sharing of URL via spoken word only, rather than having to present the URL on a screen for the other person to see and copy.

   Disadvantage: URLs may be longer, and users would need to type more characters. Another disadvantage is the url may more easily be guessable by a third party through brute force guessing, which could potentially give bad actors access to webpages that are visible to anyone with the link.

   Modifications: NonceGeneration would additionally need to keep a list of dictionary words, and 'generate' would randomly pick a couple words from the dictionary to append together to form a string.

## Synchronization

1. The generate sync is used to generate the short url suffix, so it only cares about not matching the short url base, and the target URL is irrelevant. In the register sync, the then clause calls register, which needs the targetURL and the shortUrlBase, therefore both must appear in the when clause.

2. If the variable names do not match the argument or result name, omitting names can cause confusion as to which parameter the variable is bound to.

3. The third sync is not a direct request from the user. It seems that the URL shortening application sets an automatic expiry after a URL is registered. The user is not the one setting the expiry, so there is no Request action.

4. The generate sync would not include shortUrlBase in the request, and the context for NonceGeneration would be the fixed domain. The register sync would pass in the fixed domain as the shortUrlBase.

5. **sync** expire  
   **when** ExpiringResource.expireResource () : (resource: shortUrl)  
   **then** UrlShortening.delete (shortUrl)
