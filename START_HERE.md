# Respondus Lockdown Browser Bypass - Disclosure

## Introduction

Hi! My name's Ankit, and I work as a tutor and software developer at the University of Sydney. This semester, one of the courses that I teach, INFO2222, is using the Respondus lockdown browser to conduct the unit's final exam.

## Discovery and Development

After taking my students through the installation procedure for Respondus and the unit's sample exam, I decided to look online for some vulnerabilities in the software, specifically as several of my students had experienced issues in downloading the browser (such as long periods of stalling or being forced to restart their machines). This is when I came across the following repository by @trympet on GitHub:

[Original Repository](https://github.com/trympet/lockdown-browser-bypass-macos)

The repo (last updated in 2020/21) shows how the use of a Helium browser through a pip browser window can be used to bypass the restrictions imposed by the Respondus lockdown browser by essentially running it in a localised environment on my laptop. All I've done is ask an AI IDE agent to make this work with a newer version of MacOS.

## Implementation Details

Consequentially, I gave this a shot but was unsuccessful, so in the spirit of a true modern vibe coding specialist I decided to use Cursor, a tool introduced to me during my teaching endeavours for INFO2222, to play around with this. I asked Cursor to update this by combining the existing vulnerability (which does not seem to have been fully patched, hence this updated vulnerability being reported) with a script I wrote for another project to load an AI agent concurrently in a separate isolated window. This is nothing special and is somewhat primitive (and arguably incomplete) as it's just a connection through the OpenAI API at this stage. In reality, this isn't really needed and was more of a way of seeing if I could add on my own behaviour to an agent and obscure any network traffic in case this was being monitored by Respondus. I also quite literally asked Cursor to obscure everything as much as possible in an effort to simulate a student that would just try their best to hide any evidence of wrongdoing in an exam situation where they don't want their network traffic to be visible. In reality this doesn't do much but wasn't picked up by Respondus, so I guess it worked.

In other words, the vulnerability here is running Respondus in a localised browser. The rest of the script and setup are just me playing around with the ways I can obscure information from being intercepted or read by the lockdown browser, which seems to work in favour of the vulnerability, so I've included them nonetheless. But yes, Respondus is very easily breakable on Intel Macs, and most likely on ARM Macs as well.

## Future Plans

Moving forward, if I manage to get some free time I'm going to see if i can use a version of this setup implemented in Rust combined with a framework such as Tauri to control the browser's native rendering code myself as well. This seems fairly plausible given that I essentially still have free control over my program when the Helium browser is active, so I can probably make my own little window and AI agent to chat to that is still functionally secure enough to not warrant any concerns from Respondus' perspective. I'll keep this repo updated in case I proceed with this further.

## Disclaimer

I hereby declare that the work in the repository is not my own. The majority of the work, as well as the original idea for this exploit (as well as the original repository) are property of @trympet on GitHub. Approximately 95% of the content added to this repository is AI-generated in at least some capacity. From both an educator and a developer's perspective, I'll admit it feels weird (and honestly immoral) to be pushing code that is predominantly written by AI, as this goes against my basic moral code in the work I develop, but here we are in a situation where I'm using the AI to break someone else's software. Hopefully my perils help to make Respondus more secure in the future.
