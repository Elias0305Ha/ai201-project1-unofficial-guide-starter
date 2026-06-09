import gradio as gr
from embed import build_database
from generate import answer_question

print("Setting up the database... (one moment)")
collection = build_database()
print("Ready!")


def handle_query(question):
    if not question.strip():
        return "Please type a question.", ""
    answer, sources = answer_question(collection, question)
    source_list = "\n".join(f"• {s}" for s in sources)
    return answer, source_list


def clear_all():
    return "", "", ""


with gr.Blocks(theme=gr.themes.Soft(), title="The Unofficial Guide") as demo:
    gr.Markdown(
        """
        # 🏠 The Unofficial Guide
        Honest answers about off-campus housing near **MSU Mankato** — drawn from real student reviews.
        """
    )

    with gr.Row():
        # Left column: ask
        with gr.Column(scale=1):
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. Which apartment is the cheapest?",
                lines=2,
            )
            with gr.Row():
                ask_button = gr.Button("Ask", variant="primary")
                clear_button = gr.Button("Clear")

            gr.Examples(
                examples=[
                    "Which apartment is the cheapest?",
                    "I have a car — which places have bad parking?",
                    "Which apartments are good for students with pets?",
                    "How can I protect my security deposit?",
                ],
                inputs=question_box,
            )

        # Right column: results
        with gr.Column(scale=1):
            answer_box = gr.Textbox(label="Answer", lines=8)
            sources_box = gr.Textbox(label="📄 Retrieved from", lines=4)

    ask_button.click(handle_query, inputs=question_box, outputs=[answer_box, sources_box])
    question_box.submit(handle_query, inputs=question_box, outputs=[answer_box, sources_box])
    clear_button.click(clear_all, inputs=None, outputs=[question_box, answer_box, sources_box])


if __name__ == "__main__":
    demo.launch()