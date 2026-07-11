def extract_fields(text):
    fields = {}
    for line in text.splitlines():
        if line.startswith("Project:"):
            fields["Project"] = line.replace("Project:", "").strip()
        if line.startswith("Equipment:"):
            fields["Equipment"] = line.replace("Equipment:", "").strip()
        if line.startswith("Vendor:"):
            fields["Vendor"] = line.replace("Vendor:", "").strip()
        if line.startswith("Date:"):
            fields["Date"] = line.replace("Date:", "").strip()
    return fields


def compare_fields(spec_fields, vendor_fields):
    results = []
    for key in spec_fields:
        spec_val = spec_fields[key]
        vendor_val = vendor_fields.get(key, "")
        status = "✔" if spec_val == vendor_val else "❌"
        results.append({
            "field": key,
            "spec": spec_val,
            "vendor": vendor_val,
            "status": status
        })
    return results
