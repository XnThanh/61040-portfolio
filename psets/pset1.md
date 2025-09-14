# Problem Set 1: Reading and Writing Concepts

## Exercise 1: Reading a Concept

1. Invariants. What are two invariants of the state? (Hint: one is about aggregation/counts of items, and one relates requests and purchases). Say which one is more important and why; identify the action whose design is most affected by it, and say how it preserves it.

   1. The sum of counts in purchases and counts in requests should equal the original quantity that the owner User wants.
   2. A user cannot request or purchase a non-positive amount of item.

Invariant 1 is more important because it is a functionality issue, and if the user provides valid inputs and actions, then the system should work correctly. Whereas invariant 2 is an edge case based on incorrect user behavior, either from mistake or a bad actor.

The purchase action is most affected because it changes the state of the counts. Invariant 1 is preserved in the purchase action by decrementing the count in requests when a purchase is made.

2. Fixing an action. Can you identify an action that potentially breaks this important invariant, and say how this might happen? How might this problem be fixed?

removeItem can break invariant 1 because it only deletes the request from the registry, and not all the purchases related to that request. It can be fixed by updating removeItem to also delete all relevant purchases.

3. Inferring behavior. The operational principle describes the typical scenario in which the registry is opened and eventually closed. But a concept specification often allows other scenarios. By reading the specs of the concept actions, say whether a registry can be opened and closed repeatedly. What is a reason to allow this?

The registry can be opened and closed repeatly based on different user behaviors. A wedding registry might close on a set date but then reopen because the wedding got delayed. Or the user wants to make significant changes to the registry after opening it, but want to ensure that no new purchases were made while they are making changes, so they may temporarily close the registry.

4. Registry deletion. There is no action to delete a registry. Would this matter in practice?

Yes and no. It doesn't matter so much that there isn't a delete because closing a registry makes it non-public and to the registry owner, that serves a similar purpose to delete. However, having a delete action can help with clutter. A user might have a lot of outdated registries or made duplicates, and they might not want to see them anymore on their dashboard.

5. Queries. What are two common queries likely to be executed against the concept state? (Hint: one is executed by a registry owner, and one by a giver of a gift.)

- View all purchases (registry owner)
- View all requests (gifter)

6. Hiding purchases. A common feature of gift registries is to allow the recipient to choose not to see purchases so that an element of surprise is retained. How would you augment the concept specification to support this?

Add a "hide" flag to the Registry state. Add an action hidePurchase with the following specs:

    hidePurchase (registry: Registry)
      requires registry exists
      effects make purchases in registry hidden

7. Generic types. The User and Item types are specified as generic parameters. The Item type might be populated by SKU codes, for example. Explain why this is preferable to representing items with their names, descriptions, prices, etc.

It keeps the specifications simple and modular. We can use the SKU codes to look up the item and the relevant details. It also reduces the problem of duplicate names, since different items can have the same names, price, etc. Additionally, since an item has a lot of attached data (such as price, color, size, etc.), the SKU keeps the tracking of items simple.

## Exercise 2: Extending a familiar concept

1.  Complete the definition of the concept state.

    a set of Users with  
    &emsp; a username String  
    &emsp; a password String

2.  Write a requires/effects specification for each of the two actions. (Hints: The register action creates and returns a new user. The authenticate action is primarily a guard, and doesn’t mutate the state.)

    register (username: String, password: String): (user: User)  
    &emsp; requires username does not already exist in set of Users  
    &emsp; effects create a new User with this username and password. Return new User.

    authenticate (username: String, password: String): (user: User)  
    &emsp; requires password and username matches the same User  
    &emsp; effects Return User

3.  What essential invariant must hold on the state? How is it preserved?

No two User can have the same username. This invariant is preserved by the precondition of 'register' action.

4.  One widely used extension of this concept requires that registration be confirmed by email. Extend the concept to include this functionality. (Hints: you should add (1) an extra result variable to the register action that returns a secret token that (via a sync) will be emailed to the user; (2) a new confirm action that takes a username and a secret token and completes the registration; (3) whatever additional state is needed to support this behavior.)

[Assumptions made: One email can only be associated with one account]

- Update state to include email, verification token, and verified flag:  
   a set of Users with  
   &emsp; a username String  
   &emsp; a password String  
   &emsp; an email Email  
   &emsp; a token Number  
   &emsp; a verified Flag

- Update register action:  
   register (username: String, password: String, email: Email): (user: User, token: Number)  
   &emsp; requires username does not already exist in set of Users; email does not already exist  
   &emsp; effects create a new User with this username and password. Create a secret token Number and update token in User state. Return new User and token to be sent to user email.

- Add new confirm action:  
   confirm(username: String, token: Number):  
   &emsp; requires username exists and token matches token associated with that username  
   &emsp; effects mark User as verified

## Exercise 3: Comparing concepts

### Specs

**concept**

PersonalAccessToken

**purpose**

Limit Github access as User specifies

**principle**

After a user creates a personal access token, they can use it to login and access only what they specified when creating that token.

**state**

a set of Users with  
&emsp; a username String  
&emsp; a password String  
&emsp; a set of Tokens

a set of Tokens with  
&emsp; a tokenValue String  
&emsp; a tokenName String  
&emsp; an expiration Date  
&emsp; a set of Scopes

a set of Scopes with  
&emsp; a name String

**actions**

createToken (username: String, tokenName: String expiration: Date, set of Scopes): (token: Token)  
&emsp; requires: username exists, tokenName does not already exists, expiration date in the future, Scope is not empty  
&emsp; effects: create a new token with the provided inputs (creating a new tokenValue), adds token to user associated with given username. Returns Token.

deleteToken (username: String, tokenName: String)  
&emsp; requires: username exists, tokenName exists  
&emsp; effects: delete token

authorize (username: String, tokenValue: String, scope: Scope):  
&emsp; requires: username contains token with provided tokenValue, token with tokenValue contains scope

### Differences

Personal Access Tokens differ from passwords because they have more settings you can adjust. You can set an expiration date which will render the token invalid after a certain date, and limit what access rights that token has. A password will log you in and give you all access associated with that user, but a token can reduce the scope of your access when logging in via a token. I would change the GitHub documentation to explicitly state this difference. The one sentence in the _About_ subheader was not clear to me when I first read it.

## Exercise 4

**concept**

URL Shortener

**purpose**

Shortens a URL link

**principle**

After user enters a URL and, they will receive a new, short URL.

**state**

a set of externalURL with  
&emsp; a set of internalURLs

a set of interalURLs with  
&emsp; a suffix String

**actions**

shortenAuto (externalURL: URL): URL  
&emsp; requires: external URL is a valid URL format  
&emsp; effects: generate a random string. Check that this string does not already exist in internalURLs. Create a new internalURL with that random string suffix. Return the random string appended to the shortener site domain.

shortenDefined (externalURL: URL, definedName: String): URL  
&emsp; requires: definedName does not already exist in internalURLs  
&emsp; effects: create a new internalURL with suffix definedName. Return new shortURL by appending definedName with shortener site domain

**NOTES**

- This does not account for login functionality (I don't have an account for bit.ly or tinyurl.com so I don't know what functionalities you get after logging in)
- The generated URL is short, but not neccessarily _shorter_. For example, if I entered _youtube.com_, I would get a new short URL, but not neccesarily shorter than _youtube.com_ since it was already short to begin with.
- An external URL can map to multiple internal URLs. This is mirroring the functionality of tinyURL. When entering _youtube.com_, I received back a different tinyurl each time after clearing cache.
- For simplicity, URL suffices are strings instead of alphanumeric

---

**concept**

ConferenceRoomBooking [User]

**purpose**

Allows user to book a conference room at a specific time and date.

**principle**

User can enter the timedate and room they would like to book. Allows user to book if room is free. After booking, no other users can book that room at that time. Users can also edit and delete their booking.

**state**

a set of Slots with  
&emsp; a time Time  
&emsp; a location RoomNumber

a set of Reservations with  
&emsp; an owner User  
&emsp; a slot Slot  
&emsp; a secondary User

**actions**

create (time: Time, location: RoomNumber)  
&emsp; requires: location and time combination does not already exist  
&emsp; effects: create new Slot with given time and location

delete (time: Time, location: RoomNumber)  
&emsp; requires: location and time combination exists in Slots  
&emsp; effects: delete Slot with given time and location

reserve (owner: User, time: Time, location: RoomNumber, secondary: User [optional]): Reservation  
&emsp; requires: slot at given time and location not already booked  
&emsp; effects: creates & returns a new reservation for owner User at Slot with given time and location. Attach secondary User if provided.

edit (r: Reservation, time: Time [optional], location: RoomNumber [optional], secondary: User [optional])  
&emsp; requires: r exists  
&emsp; effects: update reservation with provided inputs, if possible. If provided time and location is not available for booking, reject edit.

cancel (r: Reservation)  
&emsp; requires: r exists  
&emsp; effects: delete r from Reservations

**NOTES**

- For simplicity, Time specifies the time and date.
- Users have no restraints on how many they can book and when (one user booking multiple rooms at the same time allowed)
- A user can choose to edit a reservation but not provide any input for new changes. It would simply leave the state unchanged.

---

**concept**

BillableHoursTracking [User]

**purpose**

Allow employees to track their hours spent working on a project so that company can bill clients.

**principle**

Employee can begin a work session on a particular project, end a work session, and override a session start and end time

**state**

a set of Sessions with  
&emsp; an id Number  
&emsp; a start Time  
&emsp; an end Time  
&emsp; a project Project  
&emsp; a description String

a set of Projects with  
&emsp; a projectName String

**actions**

createProject (name: String): Project  
&emsp; requires: name does not already exist in Projects  
&emsp; effects: create and return a new Project.

deleteProject (project: Project):  
&emsp; requires: project exists, project is not currently in an active session  
&emsp; effects: delete project

start (project: Project, description: String): (id: Number)  
&emsp; requires: project to exist, project is not already part of an active session by the same user  
&emsp; effects: creates a new session with a new id, current time as start time, project, and user specified description. Return id.

end (id: Number): Session  
&emsp; requires: session id exists and does not have an end time  
&emsp; effects: records current time as end time. Return Session.

overrideStart (session: Session, newTime: Time)  
&emsp; requires: session exists, newTime is before session start time  
&emsp; effects: updates session start time with newTime.

overrideEnd (session: Session, newTime: Time)  
&emsp; requires: session exists, newTime is before session end time  
&emsp; effects: updates session end time with newTime.

deleteSession (id: Number)  
&emsp; requires: session id exists  
&emsp; effects: delete Session associated with session id.

**NOTES**

- Start and end times can only be change to earlier times, not later than original times
- Users allowed to delete a session regardless of whether it is currently active or not
