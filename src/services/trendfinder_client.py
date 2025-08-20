
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - TrendFinder MCP Client
Cliente para integração com TrendFinder MCP
"""

import os
import logging
import httpx
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class TrendFinderClient:
    """Cliente para TrendFinder MCP"""

    def __init__(self):
        """Inicializa o cliente TrendFinder"""
        self.mcp_url = os.getenv('TRENDFINDER_MCP_URL')
        self.timeout = 60
        
        if not self.mcp_url:
            logger.warning("⚠️ TRENDFINDER_MCP_URL não configurado")
        else:
            logger.info(f"🔍 TrendFinder Client inicializado: {self.mcp_url}")

    async def search(self, query: str, platforms: Optional[list] = None) -> Dict[str, Any]:
        """
        Busca tendências usando TrendFinder MCP
        
        Args:
            query: Termo de busca
            platforms: Lista de plataformas (ex: ['twitter', 'instagram', 'tiktok'])
        """
        if not self.mcp_url:
            return {
                'success': False,
                'error': 'TRENDFINDER_MCP_URL não configurado',
                'source': 'TrendFinder'
            }

        try:
            logger.info(f"🔍 Buscando tendências para: {query}")
            
            # Payload para o MCP
            payload = {
                'method': 'search_trends',
                'params': {
                    'query': query,
                    'platforms': platforms or ['twitter', 'instagram', 'tiktok', 'youtube'],
                    'limit': 50,
                    'time_range': '7d'  # últimos 7 dias
                }
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.mcp_url,
                    json=payload,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'ARQV30-TrendFinder/1.0'
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Processa os resultados
                    trends_data = {
                        'success': True,
                        'source': 'TrendFinder',
                        'query': query,
                        'timestamp': datetime.now().isoformat(),
                        'platforms_searched': platforms or ['twitter', 'instagram', 'tiktok', 'youtube'],
                        'trends': data.get('result', {}).get('trends', []),
                        'hashtags': data.get('result', {}).get('hashtags', []),
                        'viral_content': data.get('result', {}).get('viral_content', []),
                        'influencers': data.get('result', {}).get('influencers', []),
                        'sentiment': data.get('result', {}).get('sentiment', {}),
                        'total_mentions': data.get('result', {}).get('total_mentions', 0),
                        'engagement_metrics': data.get('result', {}).get('engagement_metrics', {})
                    }
                    
                    logger.info(f"✅ TrendFinder: {len(trends_data['trends'])} tendências encontradas")
                    return trends_data
                    
                else:
                    error_msg = f"Erro HTTP {response.status_code}: {response.text}"
                    logger.error(f"❌ TrendFinder erro: {error_msg}")
                    return {
                        'success': False,
                        'error': error_msg,
                        'source': 'TrendFinder'
                    }
                    
        except httpx.TimeoutException:
            error_msg = f"Timeout após {self.timeout}s"
            logger.error(f"❌ TrendFinder timeout: {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'source': 'TrendFinder'
            }
            
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            logger.error(f"❌ TrendFinder erro: {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'source': 'TrendFinder'
            }

    async def search_platform_specific(self, query: str, platform: str) -> Dict[str, Any]:
        """
        Busca específica para uma plataforma
        
        Args:
            query: Termo de busca
            platform: Plataforma específica ('twitter', 'instagram', etc.)
        """
        return await self.search(query, [platform])

    async def get_trending_hashtags(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtém hashtags em tendência
        
        Args:
            category: Categoria específica (opcional)
        """
        if not self.mcp_url:
            return {
                'success': False,
                'error': 'TRENDFINDER_MCP_URL não configurado',
                'source': 'TrendFinder'
            }

        try:
            payload = {
                'method': 'get_trending_hashtags',
                'params': {
                    'category': category,
                    'limit': 100,
                    'time_range': '24h'
                }
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.mcp_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'success': True,
                        'source': 'TrendFinder',
                        'hashtags': data.get('result', {}).get('hashtags', []),
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'success': False,
                        'error': f"HTTP {response.status_code}",
                        'source': 'TrendFinder'
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'source': 'TrendFinder'
            }

    def is_available(self) -> bool:
        """Verifica se o serviço está disponível"""
        return bool(self.mcp_url)

# Instância global
trendfinder_client = TrendFinderClient()
