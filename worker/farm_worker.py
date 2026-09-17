import json, os, sys
from gradio_client import Client

ROLE = os.environ.get('ROLE','UNKNOWN_ROLE')
MISSION = os.environ.get('MISSION','Business and market analysis')
MODEL = os.environ.get('MODEL','huggingface-projects/llama-3.2-3B-Instruct')

prompt = f'''You are CEREBRON Omega Farm 22 role: {ROLE}.
Mission: {MISSION}
Rules: REALITY > COHERENCE; CLAIM <= EVIDENCE; FORECAST != FACT; MARKET SIZE != ADDRESSABLE REVENUE; INTEREST != PURCHASE INTENT; UNIT ECONOMICS BEFORE SCALE; UNKNOWN REMAINS UNKNOWN.
Return concise structured analysis with: claims, evidence/assumptions, method, uncertainty, risks, falsification tests, and status labels FACT/DERIVED/ASSUMPTION/FORECAST/SCENARIO/UNKNOWN.
Do not pretend external verification occurred unless evidence is supplied.'''

out={'role':ROLE,'model':MODEL,'status':'UNREVIEWED_EXTERNAL_AGENT_OUTPUT'}
try:
    client=Client(MODEL, verbose=False)
    result=client.predict(prompt, api_name='/chat')
    out['result']=result
except Exception as e:
    out['error']=repr(e)
    out['status']='EXTERNAL_CALL_FAILED'

os.makedirs('results',exist_ok=True)
path=f"results/{ROLE}.json"
with open(path,'w',encoding='utf-8') as f: json.dump(out,f,ensure_ascii=False,indent=2)
print(path)
if out.get('status')=='EXTERNAL_CALL_FAILED': sys.exit(1)
