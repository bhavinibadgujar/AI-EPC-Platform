def predict(comparison):

    risks=[]

    for item in comparison:

        if item["delay"]>=5:
            level="High"

        elif item["delay"]>=2:
            level="Medium"

        else:
            level="Low"

        risks.append({
            **item,
            "risk":level
        })

    return risks    