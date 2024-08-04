import flet as ft
from src.document_finder import DocumentFinder
from src.document_gatherer import DocumentModel

def main(page: ft.Page):
    """
        Main function to set up and run the Document Search application.

        Args:
            page (ft.Page): The main page of the Flet application.
    """
    page.title = "Document Search"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    
    model = None

    def handle_add_folder(e):
        folder_path = folder_path_input.value
        if folder_path:
            document_object = DocumentFinder(folder_path)
            all_documents = document_object.get_documents()
            nonlocal model
            model = DocumentModel(all_documents)
            page.update()

    def handle_search(e):
        search_term = search_input.value
        if search_term and model:
            search_results = model.search_document(search_term, n_results=5)
            update_documents_display(search_results)

    def update_documents_display(documents_to_display):
        documents.controls.clear()
        for doc in documents_to_display:
            documents.controls.append(
                ft.Column([
                    ft.Text(f"Document: {doc['name']}", weight="bold"),
                    ft.Text(f"Path: {doc['path']}"),
                    ft.Text(f"Content preview: {doc['content']}"),
                    ft.Text(f"Similarity: {doc['similarity']:.4f}", color=ft.colors.BLUE)
                ])
            )
        page.update()

    folder_path_input = ft.TextField(label="Enter Folder Path", expand=True)
    search_input = ft.TextField(label="Enter text to search for", expand=True)
    documents = ft.Column(expand=1, scroll="always")

    page.add(
        ft.Text("Document Search", size=20, weight="bold"),
        ft.Row([
            folder_path_input,
            ft.IconButton(icon=ft.icons.FOLDER_OPEN, on_click=handle_add_folder),
        ]),
        ft.Row([
            search_input,
            ft.IconButton(icon=ft.icons.SEARCH, on_click=handle_search),
        ]),
        documents
    )

ft.app(target=main)