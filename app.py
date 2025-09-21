# integrated_enhanced_ai.py - Your Enhanced AI with Super Strong Database

import pytesseract
from PIL import Image
import io # Used to handle image bytes
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse
import feedparser
import json
from enhanced_database import EnhancedDatabase

class SuperPoweredNewsVerificationAI:
    def __init__(self):
        # --- (Your existing __init__ code remains the same) ---
        print("🚀 Loading SUPER POWERED News Verification AI...")
        
        # Load AI models
        self.fake_news_detector = pipeline("text-classification", 
                                         model="hamzab/roberta-fake-news-classification")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
        # Load enhanced database system
        self.enhanced_db = EnhancedDatabase()
        
        # RSS feeds (backup for news search)
        self.news_feeds = {
            'reuters': 'http://feeds.reuters.com/reuters/topNews',
            'bbc': 'http://feeds.bbci.co.uk/news/world/rss.xml',
            'ap': 'https://feeds.apnews.com/apnews/world',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'npr': 'https://feeds.npr.org/1001/rss.xml'
        }
        
        print("✅ SUPER POWERED AI ready with:")
        print("   📊 500+ source credibility database")
        print("   ✅ Comprehensive fact-check database") 
        print("   🔗 Google Fact Check API integration")
        print("   📰 NewsAPI integration")
        print("   🎯 Advanced pattern recognition")
        print("   🖼️ NEW: Image-to-Text (OCR) capability") # NEW
    
    # --- (All your existing methods like extract_article_text, analyze_text_content etc. remain here) ---

    # NEW: Method to extract text from an image
    def extract_text_from_image(self, image_bytes: bytes):
        """Extracts text from an image using Tesseract OCR."""
        try:
            print("🖼️ Extracting text from image...")
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            print(f"  -> Extracted {len(text)} characters.")
            if not text.strip():
                return {'error': 'No text found in the image or image is not clear enough.'}
            return {'text': text}
        except Exception as e:
            print(f"❌ OCR Error: {str(e)}")
            return {'error': f"Failed to process image. It may be a corrupted or unsupported file format. Error: {str(e)}"}

    # NEW: Comprehensive analysis specifically for text (refactored from API)
    def analyze_text_comprehensive(self, text: str):
        """Performs a full analysis on a piece of text and returns a structured result."""
        content_analysis = self.analyze_text_content(text)
        
        if 'error' in content_analysis:
            return content_analysis

        # Calculate score with content quality factors
        fake_probability = content_analysis.get('fake_probability', 0.5)
        ai_credibility = (1 - fake_probability) * 100
        
        signals = content_analysis.get('content_signals', {})
        emotional_penalty = min(signals.get('emotional_language', 0) * 8, 25)
        urgency_penalty = min(signals.get('urgency_indicators', 0) * 6, 20)
        extreme_penalty = min(signals.get('extreme_language', 0) * 2, 15)
        credible_bonus = min(signals.get('credible_language', 0) * 4, 20)
        
        content_score = max(0, 100 - emotional_penalty - urgency_penalty - extreme_penalty + credible_bonus)
        
        # For text-only: 60% AI, 40% content quality
        final_score = (ai_credibility * 0.6 + content_score * 0.4)
        
        # Generate recommendation
        if final_score >= 80:
            recommendation = "✅ HIGH CREDIBILITY - Content appears reliable"
        elif final_score >= 60:
            recommendation = "⚠️ MODERATE CREDIBILITY - Verify with additional sources"
        elif final_score >= 40:
            recommendation = "❌ LOW CREDIBILITY - Multiple concerns detected"
        else:
            recommendation = "🚫 VERY LOW CREDIBILITY - Likely misinformation"
            
        return {
            "text_analyzed": text[:300] + "..." if len(text) > 300 else text,
            "credibility_score": round(final_score, 1),
            "recommendation": {"primary_recommendation": recommendation},
            "analysis_details": {
                "ai_fake_probability": round(fake_probability, 3),
                "content_quality_score": round(content_score, 1),
                "content_signals": signals,
                "sentiment": content_analysis['sentiment'],
            }
        }

    # NEW: Orchestrator method for the complete image analysis workflow
    def analyze_image_complete(self, image_bytes: bytes):
        """Complete image analysis pipeline: OCR -> Text Analysis."""
        print(f"\n🚀 SUPER ANALYSIS of Image")
        
        # Step 1: Extract text from image
        ocr_result = self.extract_text_from_image(image_bytes)
        if 'error' in ocr_result:
            return ocr_result
        
        extracted_text = ocr_result['text']
        
        # Step 2: Analyze the extracted text using the comprehensive text analyzer
        analysis_result = self.analyze_text_comprehensive(extracted_text)
        
        # Add the extracted text to the final result for display
        analysis_result['extracted_text'] = extracted_text
        
        return analysis_result
    
    def extract_article_text(self, url):
        """Extract main article text from URL"""
        try:
            print(f"📰 Extracting article from: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'header']):
                element.decompose()
            
            # Try to find main content
            article_text = None
            article = soup.find('article')
            if article:
                article_text = article.get_text(separator=' ', strip=True)
            
            if not article_text:
                content_selectors = ['div[class*="content"]', 'div[class*="article"]', 'main']
                for selector in content_selectors:
                    content_div = soup.select_one(selector)
                    if content_div:
                        article_text = content_div.get_text(separator=' ', strip=True)
                        if len(article_text) > 200:
                            break
            
            if not article_text or len(article_text) < 200:
                article_text = soup.get_text(separator=' ', strip=True)
            
            article_text = ' '.join(article_text.split())
            
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "No title found"
            
            return {
                'text': article_text[:4000],
                'title': title,
                'length': len(article_text),
                'url': url
            }
            
        except Exception as e:
            return {'error': f"Could not extract text: {str(e)}"}
    
    def analyze_text_content(self, text):
        """Enhanced text analysis with proper error handling"""
        try:
            print("🔍 Running SUPER content analysis...")
            
            fake_result = self.fake_news_detector(text[:512])
            fake_score = fake_result[0]['score'] if fake_result[0]['label'] == 'FAKE' else 1 - fake_result[0]['score']
            
            # FIXED sentiment analysis
            try:
                sentiment_result = self.sentiment_analyzer(text[:512])
                if isinstance(sentiment_result, list) and len(sentiment_result) > 0:
                    sentiment_data = sentiment_result[0]
                    sentiment_info = {
                        'label': sentiment_data.get('label', 'NEUTRAL'),
                        'score': sentiment_data.get('score', 0.5)
                    }
                else:
                    sentiment_info = {'label': 'NEUTRAL', 'score': 0.5}
            except:
                sentiment_info = {'label': 'NEUTRAL', 'score': 0.5}
            
            content_signals = self.analyze_content_quality(text)
            
            return {
                'fake_probability': fake_score,
                'sentiment': sentiment_info,
                'content_signals': content_signals,
                'text_sample': text[:200] + "..." if len(text) > 200 else text
            }
            
        except Exception as e:
            return {
                'fake_probability': 0.5,
                'sentiment': {'label': 'NEUTRAL', 'score': 0.5},
                'content_signals': {
                    'emotional_language': 0, 'urgency_indicators': 0,
                    'credible_language': 0, 'extreme_language': 0,
                    'exclamation_marks': 0, 'all_caps_words': 0, 'question_marks': 0
                },
                'text_sample': text[:200] if text else "No text provided"
            }
    
    def analyze_content_quality(self, text):
        """Analyze text quality indicators"""
        if not text:
            return {'emotional_language': 0, 'urgency_indicators': 0, 'credible_language': 0,
                   'extreme_language': 0, 'exclamation_marks': 0, 'all_caps_words': 0, 'question_marks': 0}
        
        text_lower = text.lower()
        
        emotional_words = ['shocking', 'unbelievable', 'secret', 'exposed', 'bombshell', 'devastating']
        urgency_words = ['breaking', 'urgent', 'immediately', 'act now', 'must read']
        credible_phrases = ['according to', 'study shows', 'research indicates', 'peer-reviewed']
        extreme_words = ['always', 'never', 'everyone', 'no one', 'completely', 'totally']
        
        return {
            'emotional_language': sum(1 for word in emotional_words if word in text_lower),
            'urgency_indicators': sum(1 for word in urgency_words if word in text_lower),
            'credible_language': sum(1 for phrase in credible_phrases if phrase in text_lower),
            'extreme_language': sum(1 for word in extreme_words if word in text_lower),
            'exclamation_marks': text.count('!'),
            'all_caps_words': len([word for word in text.split() if word.isupper() and len(word) > 2]),
            'question_marks': text.count('?')
        }
    
    def check_source_credibility(self, url):
        """USE SUPER DATABASE for source checking"""
        return self.enhanced_db.check_source_credibility_enhanced(url)
    
    def simple_fact_check(self, claim):
        """USE SUPER DATABASE for fact-checking"""
        return self.enhanced_db.enhanced_fact_check(claim)
    
    def search_live_news_super(self, query, max_results=10):
        """ENHANCED news search with NewsAPI + RSS fallback"""
        print(f"🔍 SUPER news search for: '{query}'")
        
        # Try NewsAPI first (if configured)
        news_results = self.enhanced_db.search_news_with_newsapi(query, days_back=3)
        
        # If NewsAPI didn't work or returned few results, use RSS fallback
        if len(news_results) < 3:
            print("🔄 Using RSS fallback for additional results...")
            rss_results = self.search_live_news_rss(query, max_results - len(news_results))
            news_results.extend(rss_results)
        
        return news_results[:max_results]
    
    def search_live_news_rss(self, query, max_results=5):
        """RSS fallback news search"""
        results = []
        query_lower = query.lower()
        keywords = [word.strip() for word in query_lower.split() if len(word.strip()) > 3]
        
        for source_name, feed_url in self.news_feeds.items():
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:15]:
                    title = entry.get('title', '').lower()
                    summary = entry.get('summary', '').lower()
                    
                    relevance_score = 0
                    for keyword in keywords:
                        if keyword in title:
                            relevance_score += 3
                        if keyword in summary:
                            relevance_score += 1
                    
                    if relevance_score > 0:
                        # Check source credibility
                        source_check = self.check_source_credibility(f"https://{source_name}.com")
                        
                        results.append({
                            'title': entry.get('title', 'No title'),
                            'url': entry.get('link', ''),
                            'source': source_name.upper(),
                            'published': entry.get('published', 'Unknown'),
                            'description': entry.get('summary', 'No description')[:150] + "...",
                            'relevance_score': relevance_score,
                            'credibility_score': source_check['credibility_score'],
                            'source_category': source_check['category']
                        })
                
            except Exception as e:
                print(f"⚠️ Failed to check {source_name}: {e}")
                continue
        
        # Sort by relevance and credibility
        results.sort(key=lambda x: (x['relevance_score'] * 0.6 + x['credibility_score'] * 0.4), reverse=True)
        return results[:max_results]
    
    def calculate_comprehensive_score(self, content_analysis, source_analysis):
        """Calculate final credibility score"""
        ai_credibility = (1 - content_analysis.get('fake_probability', 0.5)) * 100
        source_credibility = source_analysis.get('credibility_score', 50)
        
        signals = content_analysis.get('content_signals', {})
        emotional_penalty = min(signals.get('emotional_language', 0) * 8, 25)
        urgency_penalty = min(signals.get('urgency_indicators', 0) * 6, 20)
        credible_bonus = min(signals.get('credible_language', 0) * 4, 20)
        
        content_score = max(0, 100 - emotional_penalty - urgency_penalty + credible_bonus)
        final_score = (ai_credibility * 0.40 + source_credibility * 0.35 + content_score * 0.25)
        final_score = max(0, min(100, final_score))
        
        return {
            'final_credibility_score': round(final_score, 1),
            'breakdown': {
                'ai_analysis': round(ai_credibility, 1),
                'source_credibility': source_credibility,
                'content_quality': round(content_score, 1)
            },
            'penalties_applied': {'emotional_language': emotional_penalty, 'urgency_indicators': urgency_penalty},
            'bonuses_applied': {'credible_language': credible_bonus}
        }
    
    def get_detailed_recommendation(self, score, source_info, content_signals):
        """Generate detailed recommendations"""
        recommendations = []
        
        if score >= 80:
            primary = "✅ HIGH CREDIBILITY - This appears to be reliable information"
        elif score >= 60:
            primary = "⚠️ MODERATE CREDIBILITY - Verify with additional sources"
        elif score >= 40:
            primary = "❌ LOW CREDIBILITY - Approach with significant caution"
        else:
            primary = "🚫 VERY LOW CREDIBILITY - Likely misinformation"
        
        # Enhanced recommendations based on super database
        category = source_info.get('category', 'unknown')
        if category == 'trusted':
            recommendations.append(f"✅ Source ({source_info['domain']}) is highly credible")
        elif category == 'unreliable':
            recommendations.append(f"❌ Source ({source_info['domain']}) has poor reliability record")
        elif category == 'government_academic':
            recommendations.append("✅ Government or academic source - generally reliable")
        else:
            recommendations.append("⚠️ Unknown source - verify publisher credibility")
        
        return {'primary_recommendation': primary, 'detailed_recommendations': recommendations}
    
    def analyze_url_complete(self, url):
        """Complete URL analysis with SUPER database"""
        print(f"\n🚀 SUPER ANALYSIS of: {url}")
        
        extraction_result = self.extract_article_text(url)
        if 'error' in extraction_result:
            return {'error': extraction_result['error']}
        
        content_analysis = self.analyze_text_content(extraction_result['text'])
        source_analysis = self.check_source_credibility(url)
        final_analysis = self.calculate_comprehensive_score(content_analysis, source_analysis)
        recommendations = self.get_detailed_recommendation(
            final_analysis['final_credibility_score'], source_analysis, content_analysis['content_signals']
        )
        
        return {
            'url': url,
            'article_title': extraction_result['title'],
            'analysis_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'credibility_score': final_analysis['final_credibility_score'],
            'recommendation': recommendations,
            'detailed_analysis': {
                'source_analysis': source_analysis,
                'content_analysis': content_analysis,
                'score_breakdown': final_analysis['breakdown'],
                'penalties_and_bonuses': {
                    'penalties': final_analysis['penalties_applied'],
                    'bonuses': final_analysis['bonuses_applied']
                }
            },
            'article_preview': extraction_result['text'][:300] + "..."
        }
    
    def analyze_claim_comprehensive(self, claim_text):
        """SUPER comprehensive claim analysis"""
        print(f"\n🚀 SUPER COMPREHENSIVE ANALYSIS")
        print(f"Claim: {claim_text}")
        
        try:
            # Step 1: AI content analysis
            content_analysis = self.analyze_text_content(claim_text)
            
            # Step 2: SUPER news search (NewsAPI + RSS)
            keywords = self._extract_claim_keywords(claim_text)
            news_results = self.search_live_news_super(" ".join(keywords[:3]), max_results=8)
            
            # Step 3: SUPER fact-checking (Enhanced database + Google API)
            fact_checks = self.simple_fact_check(claim_text)
            
            # Step 4: Cross-verification
            cross_verification = self.cross_verify_with_sources(claim_text, news_results, fact_checks)
            
            # Step 5: Calculate final score
            final_analysis = self._calculate_comprehensive_credibility(
                content_analysis, news_results, fact_checks, cross_verification
            )
            
            # Step 6: Generate recommendations
            recommendation = self._generate_comprehensive_recommendation(
                final_analysis, len(news_results), len(fact_checks)
            )
            
            return {
                'claim': claim_text,
                'analysis_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'credibility_score': final_analysis['final_score'],
                'analysis_type': 'super_comprehensive_real_world',
                'recommendation': recommendation,
                'detailed_analysis': {
                    'content_analysis': content_analysis,
                    'news_coverage': news_results,
                    'fact_checks': fact_checks,
                    'cross_verification': cross_verification,
                    'score_breakdown': final_analysis['breakdown']
                }
            }
            
        except Exception as e:
            print(f"❌ Super analysis error: {e}")
            return {
                'claim': claim_text,
                'analysis_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'credibility_score': 50.0,
                'analysis_type': 'super_comprehensive_real_world',
                'recommendation': {
                    'status': 'ERROR',
                    'primary_recommendation': '❌ Analysis failed - please try again',
                    'detailed_recommendations': ['Technical error occurred during analysis']
                },
                'detailed_analysis': {
                    'content_analysis': {'error': str(e)},
                    'news_coverage': [], 'fact_checks': [],
                    'cross_verification': {'error': str(e)},
                    'score_breakdown': {'error': str(e)}
                }
            }
    
    def cross_verify_with_sources(self, claim, news_results, fact_checks):
        """Enhanced cross-verification"""
        verification_score = 50
        verification_details = []
        
        if news_results:
            high_credibility_sources = 0
            total_sources = len(news_results)
            
            for article in news_results:
                if article.get('credibility_score', 50) >= 80:
                    high_credibility_sources += 1
            
            if high_credibility_sources > 0:
                source_boost = min(high_credibility_sources * 20, 40)
                verification_score += source_boost
                verification_details.append(f"{high_credibility_sources}/{total_sources} high-credibility sources found")
            
            # Analyze source diversity
            unique_sources = len(set(article.get('source', '') for article in news_results))
            if unique_sources >= 3:
                verification_score += 10
                verification_details.append(f"Covered by {unique_sources} different news organizations")
        
        if fact_checks:
            for fact_check in fact_checks:
                rating = fact_check.get('rating', '').upper()
                confidence = fact_check.get('confidence', 50)
                
                if 'VERIFIED' in rating or 'CREDIBLE' in rating:
                    verification_score += confidence * 0.3
                elif 'DEBUNKED' in rating or 'FALSE' in rating:
                    verification_score -= confidence * 0.4
                elif 'MISLEADING' in rating:
                    verification_score -= confidence * 0.2
                
                verification_details.append(f"Fact-check: {rating} ({confidence}% confidence)")
        
        verification_score = max(0, min(100, verification_score))
        
        return {
            'cross_verification_score': round(verification_score, 1),
            'verification_details': verification_details,
            'total_sources_checked': len(news_results) + len(fact_checks)
        }
    
    def _extract_claim_keywords(self, text):
        """Extract keywords for search"""
        if not text:
            return []
        words = text.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return keywords[:5]
    
    def _calculate_comprehensive_credibility(self, content_analysis, news_results, fact_checks, cross_verification):
        """Calculate comprehensive credibility score"""
        ai_score = (1 - content_analysis.get('fake_probability', 0.5)) * 100
        
        # Enhanced news scoring based on source credibility
        news_score = 0
        if news_results:
            avg_source_credibility = sum(article.get('credibility_score', 50) for article in news_results) / len(news_results)
            coverage_bonus = min(len(news_results) * 8, 40)  # Up to 40 points for coverage
            news_score = min(avg_source_credibility * 0.6 + coverage_bonus, 100)
        
        # Enhanced fact-check scoring
        fact_score = 50
        if fact_checks:
            verified_weight = 0
            total_weight = 0
            
            for fc in fact_checks:
                confidence = fc.get('confidence', 50)
                rating = fc.get('rating', '').upper()
                
                if 'VERIFIED' in rating or 'CREDIBLE' in rating:
                    verified_weight += confidence
                elif 'DEBUNKED' in rating or 'FALSE' in rating:
                    verified_weight -= confidence
                elif 'MISLEADING' in rating:
                    verified_weight -= confidence * 0.5
                
                total_weight += confidence
            
            if total_weight > 0:
                fact_score = max(0, min(100, 50 + (verified_weight / total_weight) * 50))
        
        cross_score = cross_verification.get('cross_verification_score', 50)
        
        # Weighted final score (enhanced weighting)
        final_score = (ai_score * 0.25 + news_score * 0.35 + fact_score * 0.30 + cross_score * 0.10)
        final_score = max(0, min(100, final_score))
        
        return {
            'final_score': round(final_score, 1),
            'breakdown': {
                'ai_analysis': round(ai_score, 1),
                'news_coverage': round(news_score, 1),
                'fact_checking': round(fact_score, 1),
                'cross_verification': round(cross_score, 1)
            }
        }
    
    def _generate_comprehensive_recommendation(self, analysis, news_count, fact_count):
        """Generate comprehensive recommendations"""
        score = analysis['final_score']
        
        if score >= 80:
            primary = "✅ HIGH CREDIBILITY - Well-supported by multiple reliable sources"
            status = "VERIFIED"
        elif score >= 65:
            primary = "⚠️ GOOD CREDIBILITY - Generally reliable with some verification"
            status = "LIKELY_VERIFIED"
        elif score >= 50:
            primary = "⚠️ MODERATE CREDIBILITY - Mixed signals, verify independently"
            status = "PARTIALLY_VERIFIED"
        elif score >= 35:
            primary = "❌ LOW CREDIBILITY - Multiple concerns detected"
            status = "QUESTIONABLE"
        else:
            primary = "🚫 VERY LOW CREDIBILITY - Strong misinformation indicators"
            status = "LIKELY_FALSE"
        
        recommendations = [primary]
        
        if news_count == 0:
            recommendations.append("⚠️ No recent mainstream news coverage found")
        elif news_count >= 5:
            recommendations.append(f"📰 Extensive coverage: {news_count} news sources found")
        else:
            recommendations.append(f"📰 Limited coverage: {news_count} news sources found")
        
        if fact_count > 0:
            recommendations.append(f"✅ {fact_count} fact-check results available")
        else:
            recommendations.append("🔍 No specific fact-checks found - verify with reliable sources")
        
        return {
            'status': status,
            'primary_recommendation': primary,
            'detailed_recommendations': recommendations
        }

# Test the super-powered syst
    
    ai = SuperPoweredNewsVerificationAI()
    
    # Test comprehensive claim analysis
    test_claim = "COVID-19 vaccines contain microchips and are being used to control the population"
    
    result = ai.analyze_claim_comprehensive(test_claim)
    
    print(f"\n🎯 SUPER ANALYSIS RESULTS:")
    print(f"Credibility Score: {result['credibility_score']}/100")
    print(f"Status: {result['recommendation']['status']}")
    print(f"Primary: {result['recommendation']['primary_recommendation']}")
    print(f"News Sources: {len(result['detailed_analysis']['news_coverage'])}")
    print(f"Fact Checks: {len(result['detailed_analysis']['fact_checks'])}")
    
    print("\n🎉 SUPER POWERED AI testing complete!")
    print("💪 Your system now has professional-grade capabilities!")
