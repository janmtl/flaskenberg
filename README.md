Roadmap
- Add a 'type' field to question model so that you can hardcode text vs. multiple-choice questions instead of having angular guess
- Change task.complete to task.count
- Need public key crypto or digital signatures for user verification
-- On user.create, make a private key and public key
-- The hash at the reward screen is your answers encrypted with the public key (which is available to Angular)
-- You send the hash result to your TA
- Need to be able to restore user sessions via user hash