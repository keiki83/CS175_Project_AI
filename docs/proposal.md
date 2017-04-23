---
layout: default
title: Proposal
---

## Summary of the Project
<!---
In a paragraph or so, mention the main idea behind your project. At the very least, you should have a sentence that 
clearly explains the input/output semantics of your project, i.e. what information will it take as input, andwhat 
will it produce. Mention any applications, if any, for your project.)
--->
Our team will be designing a Gladiator style environment for the AI to operate within. The AI will learn, via combat experience, to get the highest number of kills within a specified time window. The input will be the terrain surrounding the AI, as well as the position of the enemies. The output will be an action for the AI to take. Enemies will vary in density and difficulty, and the job of the AI is to decide which encounters it should fight to maximize the number of kills and which it should avoid to try and stay alive. This AI could be used in a game to assist users in deciding the correct course of action in combat scenarios.

## AI/ML Algorithms
<!--- 
In a single sentence, mention the AI and ML algorithm(s) you anticipate using for your project. It does not
have to be a detailed description of the algorithm, even the sub-area of the field is sufficient. Examples of this
include “planning with dynamic programming”, “reinforcement learning with neural function approximator”,
“deep learning for images”, “min-max tree search with pruning”, and so on.
--->
Model-Free Reinforcement learning and shortest path algorithms.

## Evaluation Plan
<!--- 
As described in class, mention how you will evaluate the success of your project. In a paragraph, focus on the
quantitative evaluation: what are the metrics, what are the baselines, how much you expect your approach to
improve the metric by, what data will you evaluate on, etc. In another paragraph, describe what qualitative analysis
you will show to verify the project works, such as what are the sanity cases for the approach, how will you visualize
the internals of the algorithm to verify it works, what’s your moonshot case, i.e. it’ll be awesome and impressive if
you get there. Note that these are not promises, we’re not going to hold you to what you say here, but we want to
see if you are able to think about evaluation of your project in a critical manner.
--->
The success of the project will be evaluated on two factors; the number of kills within a time limit and the survivability of the character. The lowest score would be zero kills and a quick death. We expect to improve the time spent alive as well as improve the number of kills in the allotted time. The highest score will be based on calculating the maximum number of possible kills based on distance and time taken to kill zombies based on maximum damage per second. A satisfactory result will have some kills and no deaths. An impressive result would be a score that surpasses a human player.

We will verify that this AI Agent works by testing it in a series of controlled situations with varying amounts and difficulties of enemies. We will observe the actions of the AI Agent in each situation to verify that it is indeed learning the actions we anticipate it to learn. It would be a great success if the AI Agent is able to learn which enemies to avoid and which enemies it can defeat and defeating them in the most efficient way possible.

## Appointment with the Instructor
<!---
One member of the group should take an appointment with the instructor in the week starting 4/23 (or 4/30, if
no slots are available). Select a time such that all members of the group can attend, unless one or more members
of your group can absolutely not make any of the available times. In the proposal page, mention the date and time
you have reserved the appointment for.
Use the following link to make your appointment: https://calendly.com/sameersingh/office-hours
--->
11:00am - Tuesday, May 2, 2017
