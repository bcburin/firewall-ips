from Firewall import Firewall
from sklearn.ensemble import RandomForestClassifier

fw = Firewall(RandomForestClassifier(max_depth=2, random_state=0), "data/log.xlsx")
accuracy, precision, recall, f1_score = fw.run()

print(f"Accuracy: {accuracy}")

for i in range(len(f1_score)):
    print(f"A precisão para a classe {i} é {precision[i]}")  
    print(f"A recall para a classe {i} é {recall[i]}")  
    print(f"O F1 Score para a classe {i} é {f1_score[i]}")  