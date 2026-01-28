# Aviator Crash Game

## Overview
A browser-based Aviator crash game with server-controlled game flow. The game runs continuously with a 7-second countdown between rounds, and the crash point is determined by the server for fairness.

## Project Structure
- `index.html` - Main game file containing all HTML, CSS, and JavaScript
- `server.py` - Flask-SocketIO server for real-time game state synchronization

## Running the Project
The project runs on a Flask-SocketIO server bound to port 5000. Start with:
```bash
python server.py
```

## Game Features
- Server-controlled game flow with 7-second countdown between rounds
- Real-time multiplier synchronization across all clients
- Betting system with configurable amount
- Airplane animation that moves as multiplier increases
- Cash out functionality before crash
- Crash point determined by server (player actions don't affect outcome)
- Provably fair crash point generation with ~4% house edge

## Game Flow
1. 7-second countdown (server-controlled)
2. Game starts - multiplier increases exponentially
3. Crash happens at server-determined point
4. 3-second pause showing "FLEW AWAY!"
5. New 7-second countdown begins

## Technical Details
- Language: Amharic (Ethiopian)
- Stack: Flask, Flask-SocketIO, Eventlet, Vanilla JavaScript
- Server: Flask-SocketIO with WebSocket
- Port: 5000

## Recent Changes
- Migrated from static HTTP server to Flask-SocketIO for real-time game state
- Implemented server-side game loop with 7-second countdown
- Crash point now determined by server, not client
- Player bets and cash-outs are independent of crash point
