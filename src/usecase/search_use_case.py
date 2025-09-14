"""Search use case for product searching across marketplaces."""

from typing import List
import asyncio

from loguru import logger

from src.types.models import SearchQuery, SearchResult, Product, MarketPlace, SearchStatus


class SearchUseCase:
    """Use case for searching products across marketplaces."""
    
    def __init__(self):
        # TODO: Initialize marketplace APIs
        self.ozon_client = None
        self.wildberries_client = None
        self.yandex_market_client = None
    
    async def search_products(self, search_query: SearchQuery) -> SearchResult:
        """Search for products across specified marketplaces."""
        
        try:
            logger.info(f"Starting search for query: {search_query.query_text}")
            
            # Update query status
            search_query.status = SearchStatus.IN_PROGRESS
            
            # Search across marketplaces concurrently
            search_tasks = []
            
            for marketplace in search_query.marketplaces:
                if marketplace == MarketPlace.OZON:
                    search_tasks.append(self._search_ozon(search_query))
                elif marketplace == MarketPlace.WILDBERRIES:
                    search_tasks.append(self._search_wildberries(search_query))
                elif marketplace == MarketPlace.YANDEX_MARKET:
                    search_tasks.append(self._search_yandex_market(search_query))
            
            # If no specific marketplaces, search all
            if not search_tasks:
                search_tasks = [
                    self._search_ozon(search_query),
                    self._search_wildberries(search_query),
                    self._search_yandex_market(search_query),
                ]
            
            # Execute searches concurrently
            marketplace_results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Combine results
            all_products = []
            for result in marketplace_results:
                if isinstance(result, list):
                    all_products.extend(result)
                elif isinstance(result, Exception):
                    logger.error(f"Marketplace search failed: {str(result)}")
            
            # Sort and filter results
            filtered_products = await self._filter_and_sort_products(
                all_products, search_query
            )
            
            # Limit results
            limited_products = filtered_products[:search_query.max_results]
            
            search_result = SearchResult(
                query_id=search_query.id or "unknown",
                products=limited_products,
                total_found=len(all_products)
            )
            
            search_query.status = SearchStatus.COMPLETED
            logger.info(f"Search completed. Found {len(limited_products)} products")
            
            return search_result
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            search_query.status = SearchStatus.FAILED
            
            return SearchResult(
                query_id=search_query.id or "unknown",
                products=[],
                total_found=0,
                error_message=str(e)
            )
    
    async def _search_ozon(self, search_query: SearchQuery) -> List[Product]:
        """Search products on OZON."""
        
        try:
            logger.info(f"Searching OZON for: {search_query.query_text}")
            
            # TODO: Implement actual OZON API integration
            # For now, return mock products
            
            mock_products = [
                Product(
                    id="ozon_1",
                    name=f"OZON Product for '{search_query.query_text}'",
                    description="High-quality product from OZON",
                    price=15000.0,
                    currency="RUB",
                    url="https://ozon.ru/product/1",
                    marketplace=MarketPlace.OZON,
                    rating=4.5,
                    reviews_count=120,
                    availability=True
                ),
                Product(
                    id="ozon_2",
                    name=f"Premium {search_query.query_text} OZON",
                    description="Premium version from OZON",
                    price=25000.0,
                    currency="RUB",
                    url="https://ozon.ru/product/2",
                    marketplace=MarketPlace.OZON,
                    rating=4.7,
                    reviews_count=89,
                    availability=True
                )
            ]
            
            return mock_products
            
        except Exception as e:
            logger.error(f"OZON search failed: {str(e)}")
            return []
    
    async def _search_wildberries(self, search_query: SearchQuery) -> List[Product]:
        """Search products on Wildberries."""
        
        try:
            logger.info(f"Searching Wildberries for: {search_query.query_text}")
            
            # TODO: Implement actual Wildberries API integration
            # For now, return mock products
            
            mock_products = [
                Product(
                    id="wb_1",
                    name=f"Wildberries {search_query.query_text}",
                    description="Quality product from Wildberries",
                    price=12000.0,
                    currency="RUB",
                    url="https://wildberries.ru/product/1",
                    marketplace=MarketPlace.WILDBERRIES,
                    rating=4.3,
                    reviews_count=256,
                    availability=True
                ),
                Product(
                    id="wb_2",
                    name=f"Best {search_query.query_text} WB",
                    description="Best choice from Wildberries",
                    price=18000.0,
                    currency="RUB",
                    url="https://wildberries.ru/product/2",
                    marketplace=MarketPlace.WILDBERRIES,
                    rating=4.6,
                    reviews_count=178,
                    availability=True
                )
            ]
            
            return mock_products
            
        except Exception as e:
            logger.error(f"Wildberries search failed: {str(e)}")
            return []
    
    async def _search_yandex_market(self, search_query: SearchQuery) -> List[Product]:
        """Search products on Yandex Market."""
        
        try:
            logger.info(f"Searching Yandex Market for: {search_query.query_text}")
            
            # TODO: Implement actual Yandex Market API integration
            # For now, return mock products
            
            mock_products = [
                Product(
                    id="ym_1",
                    name=f"Yandex Market {search_query.query_text}",
                    description="Verified product from Yandex Market",
                    price=14000.0,
                    currency="RUB",
                    url="https://market.yandex.ru/product/1",
                    marketplace=MarketPlace.YANDEX_MARKET,
                    rating=4.4,
                    reviews_count=89,
                    availability=True
                )
            ]
            
            return mock_products
            
        except Exception as e:
            logger.error(f"Yandex Market search failed: {str(e)}")
            return []
    
    async def _filter_and_sort_products(
        self, products: List[Product], search_query: SearchQuery
    ) -> List[Product]:
        """Filter and sort products based on search criteria."""
        
        filtered_products = products
        
        # Apply price filters
        if search_query.price_min is not None:
            filtered_products = [
                p for p in filtered_products 
                if p.price is None or p.price >= search_query.price_min
            ]
        
        if search_query.price_max is not None:
            filtered_products = [
                p for p in filtered_products 
                if p.price is None or p.price <= search_query.price_max
            ]
        
        # Sort by rating (descending) and then by price (ascending)
        filtered_products.sort(
            key=lambda p: (-(p.rating or 0), p.price or float('inf'))
        )
        
        return filtered_products
    
    async def get_product_details(self, product_id: str, marketplace: MarketPlace) -> Product | None:
        """Get detailed information about a specific product."""
        
        try:
            if marketplace == MarketPlace.OZON:
                return await self._get_ozon_product_details(product_id)
            elif marketplace == MarketPlace.WILDBERRIES:
                return await self._get_wildberries_product_details(product_id)
            elif marketplace == MarketPlace.YANDEX_MARKET:
                return await self._get_yandex_market_product_details(product_id)
            
        except Exception as e:
            logger.error(f"Failed to get product details: {str(e)}")
            return None
    
    async def _get_ozon_product_details(self, product_id: str) -> Product | None:
        """Get OZON product details."""
        # TODO: Implement actual API call
        return None
    
    async def _get_wildberries_product_details(self, product_id: str) -> Product | None:
        """Get Wildberries product details."""
        # TODO: Implement actual API call
        return None
    
    async def _get_yandex_market_product_details(self, product_id: str) -> Product | None:
        """Get Yandex Market product details."""
        # TODO: Implement actual API call
        return None