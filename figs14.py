"""Regenera fig_response_time.pdf y fig_validation.pdf del manuscrito.
Uso: python figs14.py resultados.json   (JSON generado por analisis_manuscrito.py --out)"""
import pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, json, sys
plt.rcParams.update({'font.family':'serif','font.size':9})
d=pd.read_csv('resultados_replicas.csv')
d=d[d.latency_s.notna()]
order=[('openai','GPT-5.5','#3366CC'),('deepseek','DeepSeek-V4-pro','#F28E2B'),('gemini','Gemini 3.1 Pro','#D62728'),('anthropic','Claude Opus 5','#2CA02C')]
m=d.groupby(['provider','case_id','language']).latency_s.mean().reset_index()
fig,axs=plt.subplots(1,2,figsize=(7,3.2),sharey=True)
for ax,lang in zip(axs,['C#','Java']):
    data=[m[(m.provider==p)&(m.language==lang)].latency_s for p,_,_ in order]
    b=ax.boxplot(data,patch_artist=True,widths=0.6,medianprops=dict(color='black'))
    for patch,(_,_,c) in zip(b['boxes'],order): patch.set_facecolor(c); patch.set_alpha(0.75)
    ax.set_xticks(range(1,5)); ax.set_xticklabels([n for _,n,_ in order],rotation=20,ha='right')
    ax.set_title(lang+f' (n = {len(data[0])} pairs)'); ax.grid(axis='y',alpha=.3)
axs[0].set_ylabel('Response time per pair (s)\n(mean of three replicas)')
fig.tight_layout(); fig.savefig('fig_response_time.pdf')
print({p:(round(m[m.provider==p].latency_s.mean(),2)) for p,_,_ in order})
e=json.load(open(sys.argv[1]))['expert_questionnaire']
fig,ax=plt.subplots(figsize=(4.6,3.0))
labs=['Practical\nusefulness','Accuracy of\nresults','Comprehen-\nsibility']
mu=[e['section_means'][k] for k in 'ABC']; sd=[e['section_sd'][k] for k in 'ABC']
ax.bar(range(3),mu,yerr=sd,capsize=5,color='#6BAED6',edgecolor='black',width=0.6)
for i,(a,s) in enumerate(zip(mu,sd)): ax.text(i+0.32,a+0.04,f'{a:.2f}',va='bottom',ha='left',fontsize=8)
ax.set_xticks(range(3)); ax.set_xticklabels(labs); ax.set_ylim(1,5.6); ax.set_yticks([1,2,3,4,5])
ax.set_ylabel('Mean rating (1–5; bars: SD)'); ax.grid(axis='y',alpha=.3)
fig.tight_layout(); fig.savefig('fig_validation.pdf')
