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

## Extend

1. **concept** Ownership  
   **purpose** Manages ownership of a shortURL  
   **principle** each short URL is associated with exactly one owner  
   **state**  
   a set of Owners with  
   &emsp;a shortURL String  
   &emsp;a username String

   **action**  
   assign (shortURL, username):  
   &emsp;**requires** no ownership exists yet for shortUrl  
   &emsp;**effects** associates shortUrl with username

   giveAccess (shortURL, username): (accessKey: Boolean)  
   &emsp;**requires** ownership exists for shortUrl  
   &emsp;**effects** returns True is username matches that assigned to shortUrl, else False

   ***

   **concept** AnalyticsTracking [shortURL]  
   **purpose** Tracks analytics for shortened URL  
   **principle** Counts how many times a shortened url is accessed.
   **state**  
   a set of Monitors with  
   &emsp;a shortURL String  
   &emsp;a count Number

   **action**  
   register (shortURL):  
   &emsp;**requires** shortURL is not already being monitored  
   &emsp;**effects** adds shortURL to Monitors with count of 0

   recordAccess (shortURL):  
   &emsp;**requires** shortURL is being monitored  
   &emsp;**effects** updates count of shortURL to += 1

   view (shortURL, accessAllowed: Boolean): (count)  
   &emsp;**requires** shortURL is being monitored, accessAllowed is True  
   &emsp;**effects** return counts associated with shortURL

   ***

2. **sync** register  
   **when**  
   Request.shortenUrl (targetUrl, shortUrlBase, username)  
   NonceGeneration.generate (): (nonce)  
   **then**  
   UrlShortening.register (shortUrlSuffix: nonce, shortUrlBase, targetUrl)  
   Ownership.assign(shortUrl, username)  
   AnalyticsTracking.register(shortUrl)

   ***

   **sync** access  
   **when**  
   Request.lookupUrl (shortUrl, username)  
   **then**  
   UrlShortening.lookup (shortUrl): (targetUrl)  
   AnalyticsTracking.recordAccess (shortUrl)

   ***

   **sync** viewAnalytics  
   **when**  
   Request.viewAnalytics (shortUrl, username)  
   **then**  
   Ownership.giveAccess (shortUrl, username): (accessKey)  
   AnalyticsTracking.view (shortUrl, accessAllowed: accessKey)

3.

- Allowing users to choose their own short URLs: Update the URLShortening so that user can choose their suffix, rather than using nonce generation. Would also need to check the the UrlBase + suffix does not already exist.

- Using the “word as nonce” strategy to generate more memorable short URLs: Implementation briefly explained in Concept Question 3 (confused why this is being asked again?)

- Including the target URL in analytics, so that lookups of different short URLs can be grouped together when they refer to the same target URL: Update AnalyticsTracking to switch from shortURL to targetURL in the state. Update the sync so that we pass in the targetUrl when calling AnalyticsTracking.

- Generate short URLs that are not easily guessed: feature not useful. URLs are in the public domain, and not a private password that needs to be secure. Additionally, if URLs are short, the possibility of using brute force to guess the URL is much higher than a longer URL.

- Supporting reporting of analytics to creators of short URLs who have not registered as user: The current implementation doesn't require registration. The analytics is attached to a username (or name) that is attached to the shortURL. So as long as creators remember the name they used when creating, they can view the analytics.
