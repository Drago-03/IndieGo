from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import json
from config import DISCORD_PUBLIC_KEY

verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))

async def handle_interaction(request: Request):
    # Verify the signature
    signature = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    
    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail="Invalid request signature")
    
    body = await request.body()
    
    try:
        verify_key.verify(f"{timestamp}{body.decode()}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        raise HTTPException(status_code=401, detail="Invalid request signature")
    
    # Parse the interaction
    interaction = json.loads(body)
    
    # Handle PING
    if interaction['type'] == 1:
        return {"type": 1}  # Return PONG
        
    # Handle commands
    if interaction['type'] == 2:
        return await handle_command(interaction)
    
    # Handle components (buttons, select menus, etc)
    if interaction['type'] == 3:
        return await handle_component(interaction)
    
    return {"type": 1}

async def handle_command(interaction):
    command = interaction['data']['name']
    
    # Example command handling
    if command == 'help':
        return {
            "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            "data": {
                "content": "Here's how to use IndieGO Bot...",
                "embeds": [{
                    "title": "IndieGO Bot Help",
                    "description": "List of available commands...",
                    "color": 0x9F7AEA
                }]
            }
        }
        
    return {
        "type": 4,
        "data": {
            "content": "Unknown command"
        }
    }

async def handle_component(interaction):
    custom_id = interaction['data']['custom_id']
    
    # Example component handling
    if custom_id.startswith('ticket_'):
        return await handle_ticket_interaction(interaction)
        
    return {
        "type": 4,
        "data": {
            "content": "Unknown component interaction"
        }
    }

async def handle_ticket_interaction(interaction):
    # Handle ticket-related interactions
    return {
        "type": 7,  # UPDATE_MESSAGE
        "data": {
            "content": "Ticket updated!",
            "components": []  # Remove buttons after handling
        }
    } 