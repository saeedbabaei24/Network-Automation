# pyATS + AI Interface Health Check

This project demonstrates how to combine pyATS/Genie parsing with AI-based analysis to automatically evaluate network interface health.

1. Loads devices from `testbed.yaml`
2. Connects to each device via CLI
3. Parses `show ip interface brief` using Genie
4. Saves:
   - Full parsed JSON
   - Compact summarized JSON
5. Sends structured data to OpenAI for analysis
6. Prints AI-generated troubleshooting recommendations
7. Disconnects cleanly



## Requirements
pip install pyats genie openai


Linux:
export OPENAI_API_KEY="your_api_key_here"


## Generated Files

For each device:

- `<device>_show_ip_int_brief_full.json`
- `<device>_show_ip_int_brief_compact.json`

Full JSON = complete parsed Genie output  
Compact JSON = summarized version sent to AI  


## AI Analysis Logic

The AI is instructed to:

- Detect unhealthy interfaces:
  - down/down
  - administratively down
  - protocol down
  - missing IP address
- Suggest likely causes
- Provide quick troubleshooting commands
- Give an overall health summary


## Automation Flow

Device  
   ↓  
pyATS parse (Genie)  
   ↓  
Structured JSON  
   ↓  
Data reduction (compact view)  
   ↓  
AI analysis  
   ↓  
Health report  
