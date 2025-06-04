## Respondus Lockdown Browser Bypass Disclosure

Introduction

Hello,

My name is Ankit, and I am a tutor and software developer at the University of Sydney. This semester, one of the courses I teach, INFO2222, utilises the Respondus lockdown browser for the unit’s final exam.

Discovery and Development

Following my students’ installation of Respondus and the unit’s sample exam, I conducted an online search for vulnerabilities in the software. Several students had encountered difficulties downloading the browser, including prolonged stalling and the need to restart their machines. During this investigation, I discovered a repository on GitHub by @trympet titled “lockdown-browser-bypass-macos” (last updated in 2020/21).

The repository demonstrates how the utilisation of a Helium browser through a pip browser window can circumvent the restrictions imposed by the Respondus lockdown browser. Essentially, it runs the browser in a localised environment on my laptop. I have subsequently requested an AI IDE agent to facilitate this with a newer version of macOS.

Implementation Details

Consequently, I endeavoured to exploit this vulnerability, but my efforts were unsuccessful. In the spirit of contemporary coding practises, I utilised Cursor, a tool introduced during my teaching of INFO2222, to investigate this matter further. I requested Cursor to update the vulnerability by combining the existing vulnerability (which appears to have been incompletely patched, necessitating the reporting of this updated vulnerability) with a script I developed for another project to concurrently load an AI agent in a separate, isolated window. While this approach is not particularly innovative or sophisticated at present, as it merely establishes a connection via the OpenAI API, it serves as a preliminary demonstration of my ability to incorporate additional behaviour into an agent and potentially conceal network traffic in the event of monitoring by Respondus.

Furthermore, I explicitly instructed Cursor to obscure any information as extensively as possible, aiming to simulate a student attempting to conceal any evidence of wrongdoing during an examination scenario where they desire to conceal their network traffic. While this approach did not yield significant results and was not detected by Respondus, it demonstrates the feasibility of such an endeavour.

In essence, the vulnerability in question involves running Respondus within a localised browser environment. The remaining script and setup constitute my experimentation with techniques to obscure information from interception or reading by the lockdown browser, which appears to be effective in favour of the vulnerability. Therefore, I have included these components despite their limited practical application. It is important to note that Respondus is highly susceptible to vulnerabilities on Intel Macs and is likely to be vulnerable on ARM Macs as well.

## Future Plans

In the future, I intend to explore further avenues for exploiting this vulnerability. I am particularly interested in investigating potential vulnerabilities on ARM Macs, as they offer a unique challenge.

Forward, if I secure some free time, I intend to explore the possibility of employing a Rust implementation of this setup, coupled with a framework such as Tauri, to directly control the browser’s native rendering code. This approach appears feasible, considering that I retain complete control over my program when the Helium browser is active. Consequently, I can create a separate window and an AI agent for communication, ensuring its functional security and avoiding any concerns from Respondus’ perspective. I will maintain this repository updated if I proceed with this further.

## Disclaimer

I hereby declare that the majority of the work in this repository is not my own. This work, along with the original concept for this exploit and the original repository, belong to @trympet on GitHub. Approximately 95% of the content added to this repository is AI-generated in at least some capacity. From both an educational and a developer’s standpoint, I acknowledge that it feels unusual and potentially unethical to contribute code predominantly written by AI, as this contradicts my fundamental moral principles in my work. However, I find myself in a situation where I am utilising the AI to exploit someone else’s software. I hope that my actions contribute to enhancing Respondus’ security in the future.
