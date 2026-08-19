"""
Programmatic OpenAPI 3.0 Spec Generator and Swagger UI HTML Renderer
"""

import json
from typing import Dict, Any
from scoutedge import __version__


def get_openapi_spec_dict() -> Dict[str, Any]:
    """Generates complete OpenAPI 3.0.3 schema dictionary for ScoutEdge REST API."""
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "ScoutEdge REST API Gateway",
            "description": "AI-Powered Sports Intelligence Infrastructure REST API for athlete evaluation, rating engine (SE-R™), player growth (PGI™), and readiness monitoring (EdgeCare™).",
            "version": __version__,
            "contact": {
                "name": "EdgeSphere Sports Intelligence Private Limited",
                "url": "https://github.com/Satyendrajnv/ScoutEdge",
            },
        },
        "servers": [
            {"url": "http://localhost:8000", "description": "Local API Server"},
        ],
        "paths": {
            "/api/v1/health": {
                "get": {
                    "summary": "Health Check",
                    "description": "Checks API server health status and returns version metadata.",
                    "responses": {
                        "200": {
                            "description": "Server is healthy",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "status": "healthy",
                                        "service": "ScoutEdge REST API Gateway",
                                        "version": __version__,
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/api/v1/evaluate": {
                "post": {
                    "summary": "Evaluate Athlete",
                    "description": "Ingests performance, scouting, and readiness signals and synthesizes complete decision intelligence.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/EvaluatePayload"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Evaluation successful",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/EvaluationResult"}
                                }
                            },
                        },
                        "400": {"description": "Invalid JSON payload"},
                    },
                }
            },
            "/api/v1/rating/ser": {
                "post": {
                    "summary": "Calculate SE-R™ Rating",
                    "description": "Computes standalone ScoutEdge Rating Engine (SE-R™) score.",
                    "responses": {
                        "200": {
                            "description": "SE-R Rating calculated",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "overall_rating": 92.5,
                                        "technical_rating": 88.0,
                                        "physical_rating": 82.0,
                                        "tactical_rating": 85.0,
                                        "confidence_score": 0.85,
                                        "percentile_rank": 90.4,
                                        "key_drivers": ["High technical proficiency observed by scouts"],
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/api/v1/readiness/edgecare": {
                "post": {
                    "summary": "Calculate EdgeCare™ Readiness",
                    "description": "Computes acute:chronic workload ratio (ACWR) and injury risk index.",
                    "responses": {
                        "200": {
                            "description": "Readiness calculated",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "readiness_index": 95.2,
                                        "acwr_ratio": 1.0,
                                        "injury_risk_category": "Low",
                                        "recommended_minutes": 90,
                                        "sustainability_score": 90.0,
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "AthleteProfile": {
                    "type": "object",
                    "properties": {
                        "athlete_id": {"type": "string"},
                        "name": {"type": "string"},
                        "sport": {"type": "string"},
                        "primary_position": {"type": "string"},
                        "birth_date": {"type": "string"},
                        "height_cm": {"type": "number"},
                        "weight_kg": {"type": "number"},
                        "current_team": {"type": "string"},
                        "league_tier": {"type": "string"},
                    },
                },
                "EvaluatePayload": {
                    "type": "object",
                    "properties": {
                        "athlete": {"$ref": "#/components/schemas/AthleteProfile"},
                        "performance_signals": {"type": "array", "items": {"type": "object"}},
                        "scout_signals": {"type": "array", "items": {"type": "object"}},
                        "readiness_signals": {"type": "array", "items": {"type": "object"}},
                        "age_years": {"type": "number"},
                    },
                },
                "EvaluationResult": {
                    "type": "object",
                    "properties": {
                        "athlete_id": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "fit_score": {"type": "number"},
                        "recommendation": {"type": "string"},
                        "explainability_reasons": {"type": "array", "items": {"type": "string"}},
                    },
                },
            }
        },
    }


def get_swagger_ui_html() -> str:
    """Returns self-contained HTML page loading Swagger UI for ScoutEdge REST API."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ScoutEdge REST API — Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
    <style>
        body {{ margin: 0; padding: 0; background: #0b0f19; }}
        .swagger-ui {{ filter: invert(88%) hue-rotate(180deg); }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        window.onload = function() {{
            SwaggerUIBundle({{
                url: "/api/v1/openapi.json",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ]
            }});
        }};
    </script>
</body>
</html>"""
