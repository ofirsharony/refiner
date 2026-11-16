import html
import json

from diff_match_patch import diff_match_patch


def create_html_diff(before_text, after_text):
    """Generate styled HTML for comparing two texts side-by-side with differences highlighted using diff-match-patch."""
    dmp = diff_match_patch()
    diffs = dmp.diff_main(before_text, after_text)
    dmp.diff_cleanupSemantic(diffs)

    left_html = ""
    right_html = ""

    for op, data in diffs:
        data = html.escape(data)
        if op == -1:  # Deletion in "before" (red)
            left_html += f"<span style='color: red;'>{data}</span>"
        elif op == 1:  # Addition in "after" (green)
            right_html += f"<span style='color: green;'>{data}</span>"
        elif op == 0:  # No change
            left_html += f"{data}"
            right_html += f"{data}"

    # json.dumps makes a valid JS string, so backticks and quotes in the text don't break the button. Escape it for the attribute.
    clipboard_js = html.escape(f"navigator.clipboard.writeText({json.dumps(after_text)})")

    combined_html = f"""
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4 style='background-color: #f0f0f0; padding: 10px;'>Before</h4>
            <div>{left_html}</div>
        </div>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4 style='background-color: #f0f0f0; padding: 10px; display: flex; align-items: center; justify-content: space-between;'>
                After
                <button onclick="{clipboard_js}" style="padding: 4px 8px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-left: 10px;">
                    Copy to Clipboard
                </button>
            </h4>
            <div>{right_html}</div>
        </div>
    </div>
    """
    return combined_html
