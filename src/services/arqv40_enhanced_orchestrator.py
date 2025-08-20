
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV40 Enhanced - Orquestrador Principal
Sistema de análise ultra-profunda conforme livro técnico
"""

import os
import logging
import time
import asyncio
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

# Importa serviços conforme arquitetura do livro
from services.alibaba_websailor import alibaba_websailor
from services.supadata_mcp_client import supadata_client
from services.visual_content_capture import visual_content_capture
from services.enhanced_ai_manager import enhanced_ai_manager
from services.enhanced_module_processor import enhanced_module_processor
from services.comprehensive_report_generator_v3 import comprehensive_report_generator_v3
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class ARQV40EnhancedOrchestrator:
    """Orquestrador principal do ARQV40 Enhanced"""

    def __init__(self):
        """Inicializa o orquestrador"""
        self.current_session = None
        self.study_duration = 300  # 5 minutos em segundos
        
        logger.info("🎯 ARQV40 Enhanced Orchestrator inicializado")

    async def execute_complete_analysis(
        self, 
        produto: str, 
        nicho: str, 
        publico: str, 
        session_id: str
    ) -> Dict[str, Any]:
        """
        Executa análise completa em 3 etapas conforme livro técnico
        
        Args:
            produto: Produto a ser analisado
            nicho: Nicho de mercado
            publico: Público-alvo
            session_id: ID da sessão
        """
        logger.info(f"🚀 INICIANDO ARQV40 ENHANCED - Sessão: {session_id}")
        start_time = time.time()
        
        self.current_session = session_id
        
        try:
            # ===== ETAPA 1: COLETA MASSIVA DE DADOS =====
            logger.info("🔍 ETAPA 1: Coleta Massiva de Dados")
            etapa1_result = await self._execute_etapa1_coleta_massiva(
                produto, nicho, publico, session_id
            )
            
            if not etapa1_result.get("success"):
                raise Exception("Falha na Etapa 1: Coleta Massiva")
            
            # ===== ETAPA 2: ESTUDO PROFUNDO COM IA =====
            logger.info("🧠 ETAPA 2: Estudo Profundo com IA (5 minutos)")
            etapa2_result = await self._execute_etapa2_estudo_profundo(
                session_id, etapa1_result["relatorio_gigante"]
            )
            
            if not etapa2_result.get("success"):
                raise Exception("Falha na Etapa 2: Estudo Profundo")
            
            # ===== ETAPA 3: GERAÇÃO DE RELATÓRIO FINAL =====
            logger.info("📋 ETAPA 3: Geração de Relatório Final")
            etapa3_result = await self._execute_etapa3_relatorio_final(
                session_id, etapa2_result["contexto_aprofundado"]
            )
            
            # Resultado final
            total_time = time.time() - start_time
            
            final_result = {
                "success": True,
                "session_id": session_id,
                "etapas_completadas": 3,
                "tempo_total": f"{total_time:.2f}s",
                "etapa1_dados": etapa1_result,
                "etapa2_estudo": etapa2_result, 
                "etapa3_relatorio": etapa3_result,
                "relatorio_final_path": etapa3_result.get("relatorio_path"),
                "modulos_gerados": etapa3_result.get("modulos_count", 0),
                "timestamp": datetime.now().isoformat()
            }
            
            # Salva resultado completo
            salvar_etapa("arqv40_analise_completa", final_result, categoria="analise_completa")
            
            logger.info(f"✅ ARQV40 ENHANCED CONCLUÍDO em {total_time:.2f}s")
            logger.info(f"📊 {etapa3_result.get('modulos_count', 0)} módulos gerados")
            
            return final_result
            
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO no ARQV40: {e}")
            salvar_erro("arqv40_analise_completa", e, contexto={
                "produto": produto,
                "nicho": nicho, 
                "publico": publico,
                "session_id": session_id
            })
            
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }

    async def _execute_etapa1_coleta_massiva(
        self, 
        produto: str, 
        nicho: str, 
        publico: str, 
        session_id: str
    ) -> Dict[str, Any]:
        """ETAPA 1: Coleta Massiva de Dados"""
        
        logger.info("🔍 Iniciando Etapa 1: Coleta Massiva de Dados")
        
        # Constrói query de busca
        query_parts = [p for p in [produto, nicho, publico] if p]
        query = " ".join(query_parts) if query_parts else "análise de mercado"
        
        context = {
            "produto": produto,
            "nicho": nicho, 
            "publico": publico,
            "session_id": session_id
        }
        
        try:
            # 1.1 - Navegação Web Profunda com Alibaba WebSailor
            logger.info("🌐 1.1 - Executando Alibaba WebSailor...")
            websailor_results = alibaba_websailor.navigate_and_research_deep(
                query=query,
                context=context,
                max_pages=30,
                depth_levels=3,
                session_id=session_id
            )
            
            # 1.2 - Dados Sociais via Supadata MCP
            logger.info("📊 1.2 - Executando Supadata MCP...")
            if supadata_client.is_available():
                supadata_results = await supadata_client.search(query, "all")
                
                # Busca perfis e hashtags relevantes
                if supadata_results.get("success"):
                    profiles_data = await supadata_client.get_profile_analytics(
                        f"{produto} {nicho}", "instagram"
                    )
                    hashtag_data = await supadata_client.get_hashtag_analytics(
                        produto.replace(" ", ""), ["instagram", "twitter", "tiktok"]
                    )
                    
                    supadata_results.update({
                        "profiles_analytics": profiles_data,
                        "hashtag_analytics": hashtag_data
                    })
            else:
                logger.warning("⚠️ Supadata MCP não disponível")
                supadata_results = {"success": False, "error": "Supadata não configurado"}
            
            # 1.3 - Screenshots e Conteúdo Visual
            logger.info("📸 1.3 - Executando Visual Content Capture...")
            
            # Coleta URLs das fontes encontradas
            all_urls = self._extract_urls_from_results(websailor_results, supadata_results)
            
            if all_urls:
                visual_results = await visual_content_capture.capture_screenshots(
                    all_urls[:15], session_id  # Máximo 15 URLs
                )
            else:
                visual_results = {"success": False, "error": "Nenhuma URL encontrada"}
            
            # 1.4 - Gera Relatório Gigante MD
            relatorio_gigante = await self._generate_massive_md_report(
                websailor_results, supadata_results, visual_results, context, session_id
            )
            
            return {
                "success": True,
                "websailor_data": websailor_results,
                "supadata_data": supadata_results,
                "visual_data": visual_results,
                "relatorio_gigante": relatorio_gigante,
                "total_urls_captured": len(all_urls),
                "screenshots_count": visual_results.get("successful_captures", 0),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na Etapa 1: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_etapa2_estudo_profundo(
        self, 
        session_id: str, 
        relatorio_gigante: str
    ) -> Dict[str, Any]:
        """ETAPA 2: Estudo Profundo com IA (5 minutos)"""
        
        logger.info("🧠 Iniciando Etapa 2: Estudo Profundo com IA")
        start_study = time.time()
        
        try:
            if not enhanced_ai_manager:
                raise Exception("Enhanced AI Manager não disponível")
            
            # Prompt para estudo profundo de 5 minutos
            study_prompt = f"""
# VOCÊ É O ANALISTA ESTRATÉGICO MASTER - ESTUDO ULTRA-PROFUNDO

Você tem exatamente 5 MINUTOS para estudar profundamente este relatório gigante e se tornar um EXPERT absoluto no contexto apresentado.

## SUA MISSÃO:
1. LEIA E ABSORVA todo o conteúdo do relatório
2. IDENTIFIQUE padrões, tendências e insights ocultos
3. FAÇA buscas online para validar e enriquecer informações
4. TORNE-SE um especialista no mercado/produto analisado
5. PREPARE o contexto aprofundado para a geração dos 16 módulos

## RELATÓRIO PARA ESTUDO:
{relatorio_gigante}

## INSTRUÇÕES DE ESTUDO:
- Use google_search para buscar dados complementares
- Valide informações encontradas
- Identifique gaps de conhecimento e preencha-os
- Busque casos de sucesso e benchmarks
- Analise concorrência e oportunidades
- Entenda profundamente o público-alvo
- Mapeie o mercado completamente

## RESULTADO ESPERADO:
Retorne um JSON estruturado com seu aprendizado profundo:

```json
{{
  "contexto_aprofundado": {{
    "mercado_detalhado": "Análise ultra-detalhada do mercado",
    "publico_refinado": "Perfil refinado do público-alvo",
    "concorrencia_mapeada": "Mapeamento completo da concorrência", 
    "oportunidades_descobertas": ["Lista de oportunidades"],
    "tendencias_validadas": ["Tendências validadas online"],
    "insights_exclusivos": ["Insights únicos descobertos"],
    "dados_validados": ["Dados validados via busca"],
    "expertise_level": "EXPERT",
    "tempo_estudo": "300 segundos",
    "buscas_realizadas": 15
  }}
}}
```

INICIE O ESTUDO AGORA!
"""
            
            # Executa estudo de 5 minutos
            logger.info("⏰ Iniciando estudo intensivo de 5 minutos...")
            
            study_result = await enhanced_ai_manager.generate_with_active_search(
                prompt=study_prompt,
                context="",
                session_id=session_id,
                max_search_iterations=15,
                max_time_seconds=300  # 5 minutos
            )
            
            study_time = time.time() - start_study
            
            # Processa resultado do estudo
            contexto_aprofundado = self._process_study_result(study_result)
            
            # Salva contexto aprofundado
            session_dir = Path(f"analyses_data/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            context_path = session_dir / "contexto_aprofundado.json"
            with open(context_path, 'w', encoding='utf-8') as f:
                import json
                json.dump(contexto_aprofundado, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Estudo concluído em {study_time:.2f}s")
            
            return {
                "success": True,
                "contexto_aprofundado": contexto_aprofundado,
                "tempo_estudo": study_time,
                "buscas_realizadas": self._count_searches(study_result),
                "context_path": str(context_path),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na Etapa 2: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_etapa3_relatorio_final(
        self, 
        session_id: str, 
        contexto_aprofundado: Dict[str, Any]
    ) -> Dict[str, Any]:
        """ETAPA 3: Geração de Relatório Final (16 módulos)"""
        
        logger.info("📋 Iniciando Etapa 3: Geração de Relatório Final")
        
        try:
            # Gera os 16 módulos usando o Enhanced Module Processor
            modules_result = await enhanced_module_processor.process_all_modules(
                session_id=session_id,
                synthesis_data=contexto_aprofundado,
                use_enhanced_context=True
            )
            
            if not modules_result.get("success"):
                raise Exception("Falha na geração dos módulos")
            
            # Compila relatório final
            final_report = comprehensive_report_generator_v3.compile_final_markdown_report(
                session_id
            )
            
            if not final_report.get("success"):
                raise Exception("Falha na compilação do relatório final")
            
            return {
                "success": True,
                "modulos_gerados": modules_result.get("modules_generated", []),
                "modulos_count": len(modules_result.get("modules_generated", [])),
                "relatorio_path": final_report.get("report_path"),
                "estatisticas_relatorio": final_report.get("estatisticas_relatorio"),
                "modules_result": modules_result,
                "final_report": final_report,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na Etapa 3: {e}")
            return {"success": False, "error": str(e)}

    def _extract_urls_from_results(
        self, 
        websailor_results: Dict[str, Any], 
        supadata_results: Dict[str, Any]
    ) -> list:
        """Extrai URLs dos resultados para screenshots"""
        urls = []
        
        try:
            # URLs do WebSailor
            if websailor_results.get("conteudo_consolidado"):
                fontes = websailor_results["conteudo_consolidado"].get("fontes_detalhadas", [])
                for fonte in fontes:
                    if fonte.get("url"):
                        urls.append(fonte["url"])
            
            # URLs do Supadata
            if supadata_results.get("success") and supadata_results.get("posts"):
                for post in supadata_results["posts"][:10]:
                    if post.get("url"):
                        urls.append(post["url"])
            
            # Remove duplicatas
            return list(set(urls))
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair URLs: {e}")
            return []

    async def _generate_massive_md_report(
        self,
        websailor_results: Dict[str, Any],
        supadata_results: Dict[str, Any], 
        visual_results: Dict[str, Any],
        context: Dict[str, Any],
        session_id: str
    ) -> str:
        """Gera relatório gigante MD com todos os dados coletados"""
        
        report = f"""# RELATÓRIO GIGANTE - ARQV40 Enhanced

**Sessão:** {session_id}  
**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Produto:** {context.get('produto', 'N/A')}  
**Nicho:** {context.get('nicho', 'N/A')}  
**Público:** {context.get('publico', 'N/A')}

---

## ETAPA 1: COLETA MASSIVA DE DADOS

### 1.1 NAVEGAÇÃO WEB PROFUNDA (Alibaba WebSailor)

**Páginas Analisadas:** {websailor_results.get('navegacao_profunda', {}).get('total_paginas_analisadas', 0)}  
**Engines Utilizados:** {', '.join(websailor_results.get('navegacao_profunda', {}).get('engines_utilizados', []))}  
**Qualidade Média:** {websailor_results.get('navegacao_profunda', {}).get('qualidade_media', 0):.2f}

#### Insights Principais:
"""
        
        # Adiciona insights do WebSailor
        insights = websailor_results.get('conteudo_consolidado', {}).get('insights_principais', [])
        for i, insight in enumerate(insights, 1):
            report += f"{i}. {insight}\n"
        
        # Adiciona tendências identificadas
        report += "\n#### Tendências Identificadas:\n"
        tendencias = websailor_results.get('conteudo_consolidado', {}).get('tendencias_identificadas', [])
        for tendencia in tendencias:
            report += f"- {tendencia}\n"
        
        # Adiciona oportunidades
        report += "\n#### Oportunidades Descobertas:\n"
        oportunidades = websailor_results.get('conteudo_consolidado', {}).get('oportunidades_descobertas', [])
        for oportunidade in oportunidades:
            report += f"- {oportunidade}\n"
        
        # Dados do Supadata MCP
        report += f"\n### 1.2 DADOS SOCIAIS (Supadata MCP)\n\n"
        
        if supadata_results.get("success"):
            report += f"**Posts Coletados:** {supadata_results.get('total_results', 0)}  \n"
            report += f"**Plataformas:** {', '.join(supadata_results.get('platforms_analyzed', []))}  \n"
            
            # Posts mais relevantes
            posts = supadata_results.get("posts", [])
            if posts:
                report += "\n#### Posts Mais Relevantes:\n"
                for i, post in enumerate(posts[:10], 1):
                    title = post.get('title', post.get('content', 'Post sem título'))[:100]
                    report += f"**{i}.** {title}...\n"
                    if post.get('engagement_metrics'):
                        metrics = post['engagement_metrics']
                        report += f"   - Engajamento: {metrics.get('total_engagement', 0)}\n"
                    report += "\n"
            
            # Analytics de perfis
            if supadata_results.get("profiles_analytics"):
                report += "\n#### Analytics de Perfis:\n"
                profiles = supadata_results["profiles_analytics"]
                report += f"Perfis analisados: {profiles.get('profiles_count', 0)}\n"
            
            # Analytics de hashtags
            if supadata_results.get("hashtag_analytics"):
                report += "\n#### Analytics de Hashtags:\n"
                hashtags = supadata_results["hashtag_analytics"]
                report += f"Hashtags analisadas: {len(hashtags.get('hashtags', []))}\n"
        else:
            report += f"**Status:** Falha - {supadata_results.get('error', 'Erro desconhecido')}\n"
        
        # Conteúdo Visual
        report += f"\n### 1.3 CONTEÚDO VISUAL (Screenshots)\n\n"
        
        if visual_results.get("success"):
            report += f"**Screenshots Capturados:** {visual_results.get('successful_captures', 0)}  \n"
            report += f"**URLs Processadas:** {visual_results.get('total_urls', 0)}  \n"
            
            screenshots = visual_results.get("screenshots", [])
            if screenshots:
                report += "\n#### Evidências Visuais:\n"
                for i, screenshot in enumerate(screenshots, 1):
                    report += f"\n##### Screenshot {i}\n"
                    report += f"**URL:** {screenshot.get('url', 'N/A')}  \n"
                    report += f"**Título:** {screenshot.get('title', 'N/A')}  \n"
                    report += f"**Arquivo:** {screenshot.get('filename', 'N/A')}  \n"
                    report += f"![Screenshot {i}]({screenshot.get('filepath', '')})  \n"
        else:
            report += f"**Status:** Falha - {visual_results.get('error', 'Erro desconhecido')}\n"
        
        # Fontes Detalhadas
        report += "\n## FONTES DETALHADAS\n\n"
        fontes = websailor_results.get('conteudo_consolidado', {}).get('fontes_detalhadas', [])
        for i, fonte in enumerate(fontes, 1):
            report += f"### Fonte {i}\n"
            report += f"**URL:** {fonte.get('url', 'N/A')}  \n"
            report += f"**Título:** {fonte.get('title', 'N/A')}  \n"
            report += f"**Qualidade:** {fonte.get('quality_score', 0):.2f}  \n"
            report += f"**Engine:** {fonte.get('search_engine', 'N/A')}  \n"
            report += "\n"
        
        # Estatísticas de Coleta
        report += f"\n## ESTATÍSTICAS DE COLETA\n\n"
        report += f"- **Páginas Web Analisadas:** {websailor_results.get('navegacao_profunda', {}).get('total_paginas_analisadas', 0)}\n"
        report += f"- **Posts Sociais Coletados:** {supadata_results.get('total_results', 0)}\n"
        report += f"- **Screenshots Capturados:** {visual_results.get('successful_captures', 0)}\n"
        report += f"- **Engines Utilizados:** {len(websailor_results.get('navegacao_profunda', {}).get('engines_utilizados', []))}\n"
        report += f"- **Fontes de Qualidade Alta:** {len([f for f in fontes if f.get('quality_score', 0) > 80])}\n"
        
        report += f"\n---\n\n*Relatório gerado automaticamente pelo ARQV40 Enhanced em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*"
        
        # Salva o relatório gigante
        session_dir = Path(f"analyses_data/{session_id}")
        session_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = session_dir / "relatorio_gigante.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"📄 Relatório gigante salvo: {report_path}")
        logger.info(f"📊 Tamanho do relatório: {len(report):,} caracteres")
        
        return report

    def _process_study_result(self, study_result: str) -> Dict[str, Any]:
        """Processa resultado do estudo profundo"""
        try:
            import json
            
            # Tenta extrair JSON da resposta
            if "```json" in study_result:
                start = study_result.find("```json") + 7
                end = study_result.rfind("```")
                json_text = study_result[start:end].strip()
                return json.loads(json_text)
            
            # Fallback
            return {
                "contexto_aprofundado": {
                    "mercado_detalhado": "Análise baseada no estudo do relatório gigante",
                    "publico_refinado": "Perfil refinado através da IA",
                    "concorrencia_mapeada": "Mapeamento via análise profunda",
                    "oportunidades_descobertas": ["Oportunidades identificadas no estudo"],
                    "tendencias_validadas": ["Tendências validadas pela IA"],
                    "insights_exclusivos": ["Insights únicos do estudo"],
                    "expertise_level": "EXPERT",
                    "tempo_estudo": "300 segundos"
                },
                "raw_study": study_result[:2000],
                "fallback_mode": True
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar estudo: {e}")
            return {"error": str(e), "raw_study": study_result[:1000]}

    def _count_searches(self, text: str) -> int:
        """Conta buscas realizadas no texto"""
        search_indicators = ['busca realizada', 'search performed', 'dados encontrados']
        count = 0
        text_lower = text.lower()
        for indicator in search_indicators:
            count += text_lower.count(indicator)
        return max(count, 1)

# Instância global
arqv40_enhanced_orchestrator = ARQV40EnhancedOrchestrator()
