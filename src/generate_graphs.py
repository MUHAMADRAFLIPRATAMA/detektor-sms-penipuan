import csv, json
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from joblib import load

ROOT=Path(__file__).resolve().parent.parent
rows=list(csv.DictReader((ROOT/'data/dataset_processed/messages.csv').open(encoding='utf-8')))
texts=[r['text'] for r in rows]; labels=[int(r['label']) for r in rows]
_, x_test, _, y_test=train_test_split(texts, labels, test_size=.2, random_state=42, stratify=labels)
model=load(ROOT/'models/fraud_detector.joblib'); pred=model.predict(x_test)
metrics=json.loads((ROOT/'models/evaluation.json').read_text(encoding='utf-8'))
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax=plt.subplots(1,3,figsize=(15,4.8))
counts=[labels.count(0),labels.count(1)]
ax[0].bar(['Normal','Penipuan'],counts,color=['#2e86de','#e74c3c']); ax[0].set_title('Distribusi Dataset'); ax[0].set_ylabel('Jumlah Pesan')
for i,v in enumerate(counts): ax[0].text(i,v+30,str(v),ha='center',fontweight='bold')
cm=confusion_matrix(y_test,pred,labels=[0,1]); ConfusionMatrixDisplay(cm,display_labels=['Normal','Penipuan']).plot(ax=ax[1],cmap='Blues',colorbar=False); ax[1].set_title('Confusion Matrix')
vals=[metrics['accuracy'],metrics['report']['normal']['f1-score'],metrics['report']['penipuan']['f1-score']]
ax[2].bar(['Accuracy','F1 Normal','F1 Penipuan'],vals,color=['#27ae60','#3498db','#e67e22']); ax[2].set_ylim(0,1.08); ax[2].set_title('Hasil Evaluasi'); ax[2].set_ylabel('Skor')
for i,v in enumerate(vals): ax[2].text(i,v+.025,f'{v:.2%}',ha='center',fontweight='bold')
fig.suptitle('Detektor Pesan Penipuan - Hasil Machine Learning',fontsize=14,fontweight='bold'); fig.tight_layout()
out=ROOT/'models/hasil_grafik.png'; fig.savefig(out,dpi=180,bbox_inches='tight'); print(out)
print(json.dumps({'confusion_matrix':cm.tolist(),'accuracy':metrics['accuracy'],'f1_penipuan':metrics['f1_penipuan']},indent=2))
