from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from documents.models import Document

@tool
def list_documents(config:RunnableConfig):
    """
        List most recent 5  documents for the current user
    """
    print(config)
    limit = 5 
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    qs = Document.objects.filter(owner_id=user_id,active=True).order_by("-created_at")
    response_data = []
    for obj in qs[:limit]:
        response_data.append({
            "id": obj.id,
            "title": obj.title
        })
    return response_data    

@tool
def get_document(document_id:int,config:RunnableConfig):
    """
    Get the details of adocument for current user
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    try:
        obj = Document.objects.get(id=document_id,owner_id=user_id,active=True)
    except Document.objects.DoesNotExis:
        raise Exception("Document not found , try again")
    except:
        raise Exception("except request for a document detail ,try again")
    response_data = {
           "id": obj.id,
           "title": obj.title,
           "content": obj.content,
           "created_at": obj.created_at
       }
    return response_data


@tool
def create_document(title:str,content:str,config:RunnableConfig):
    """
    Create a new Document for the user.
    title: string max character of 120
    content: long form text in many paragraphs or pages
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    obj = Document.objects.create(title=title,content=content,owner_id=user_id,active=True)
    response_data = {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    return response_data



@tool
def update_document(document_id:int,title:str = None,content:str = None, config:RunnableConfig = None):
    """
    update a Document for the user.
    Arguments re:
    title: string max character of 120(opt)
    document_id: id of document (req)
    content: long form text in many paragraphs or pages
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    try:
        obj = Document.objects.get(id=document_id,owner_id=user_id,active=True)
    except Document.objects.DoesNotExis:
        raise Exception("Document not found , try again")
    except:
        raise Exception("except request for a document detail ,try again")
    
    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content    
    if title or content: 
        obj.save    
    response_data = {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    return response_data


@tool
def delete_document(document_id:int,config:RunnableConfig):
    """
    Delete the Document for the currrent user by document id 
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    try:
        obj = Document.objects.get(id=document_id,owner_id=user_id,active=True)
    except Document.objects.DoesNotExis:
        raise Exception("Document not found , try again")
    except:
        raise Exception("except request for a document detail ,try again")
    obj.delete()
    response_data = {
          "message":""
       }
    return response_data





document_tools = [
    list_documents , get_document ,create_document , delete_document
]