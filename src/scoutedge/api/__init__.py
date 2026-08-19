"""
ScoutEdge REST API Gateway Subsystem
"""

from scoutedge.api.server import create_scoutedge_app, ScoutEdgeHTTPRequestHandler

__all__ = ["create_scoutedge_app", "ScoutEdgeHTTPRequestHandler"]
