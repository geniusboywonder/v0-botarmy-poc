# Workflow Examples - Real-World Use Cases

**Part of:** MCP-Based Role-Constrained Agent Orchestration  
**Focus:** Concrete examples of multi-agent workflows in action

---

## Comprehensive Use Case Walkthroughs

This document provides detailed examples of how the MCP-based agent orchestration system handles real-world scenarios, showing the complete flow from user input to final deliverables.

---

## Example 1: E-Commerce Platform Development

### User Input
> "I want to build a modern e-commerce platform for selling handmade crafts. It should handle payments, inventory, and have a mobile app."

### Intent Classification Result
```json
{
  "primary_domain": "product_development",
  "complexity": "complex",
  "required_agents": ["business_analyst", "technical_architect", "developer", "qa_tester"],
  "keywords": ["build", "e-commerce", "platform", "payments", "inventory", "mobile"],
  "entities": ["handmade crafts", "payments", "inventory", "mobile app"],
  "confidence": 0.94
}
```

### Workflow Execution

#### Phase 1: Business Analysis (8 minutes)

**🤖 Business Analyst Agent Started**

*Thinking Process:* "I need to understand the business requirements for this e-commerce platform. Let me analyze the target market, key features, and success criteria."

**Analysis Output:**
```markdown
# Business Requirements Analysis - Handmade Crafts E-Commerce Platform

## Business Overview
- **Target Market**: Artisans selling handmade crafts and their customers
- **Business Model**: Commission-based marketplace (5-8% per transaction)
- **Revenue Streams**: Transaction fees, premium seller subscriptions, advertising

## Core Requirements
1. **Seller Management**
   - Artisan onboarding and verification
   - Shop customization and branding
   - Inventory management with craft-specific attributes

2. **Product Catalog**
   - Rich product descriptions with story/origin
   - High-quality image galleries
   - Custom product variations (size, color, materials)

3. **Customer Experience**
   - Advanced search and filtering
   - Wishlist and favorites
   - Review and rating system

4. **Transaction Management**
   - Secure payment processing (Stripe/PayPal)
   - Order tracking and fulfillment
   - Dispute resolution system

## Success Metrics
- **Year 1**: 500+ active sellers, 10,000+ products listed
- **Conversion Rate**: 3-5% target
- **Customer Retention**: 70% after first purchase
- **Average Order Value**: $45-60

## Stakeholder Map
- **Primary**: Craft artisans, craft buyers
- **Secondary**: Payment processors, shipping providers
- **Internal**: Development team, customer support, marketing

## Risk Assessment
- **High**: Payment security, seller verification
- **Medium**: Mobile app adoption, search performance
- **Low**: Basic catalog management
```

**Human Approval Gate: Requirements Review**
> ✅ User Approved: "Great analysis! Can you also include social features like following favorite artisans?"

**Updated Requirements:**
- Added social features: artisan following, customer reviews, social sharing

---

#### Phase 2: Technical Architecture (12 minutes)

**🤖 Technical Architect Agent Started**

*Thinking Process:* "Based on the business requirements, I need to design a scalable architecture that supports high-quality images, complex search, secure payments, and mobile access."

**Architecture Output:**
```markdown
# Technical Architecture - Handmade Crafts E-Commerce Platform

## System Architecture Overview
- **Architecture Pattern**: Microservices with API Gateway
- **Deployment**: Containerized services on Kubernetes
- **Database Strategy**: PostgreSQL primary + Redis cache + Elasticsearch search

## Core Services Architecture

### Frontend Applications
1. **Web Application**
   - Framework: Next.js 14 (React + SSR)
   - Styling: Tailwind CSS + shadcn/ui
   - State Management: Zustand
   - Authentication: NextAuth.js

2. **Mobile Applications**
   - Cross-platform: React Native with Expo
   - Native navigation and payments integration
   - Offline-first for browsing

### Backend Microservices

1. **API Gateway Service**
   - Technology: Kong or AWS API Gateway
   - Features: Rate limiting, authentication, routing
   - Load balancing across services

2. **User Management Service**
   - Authentication and authorization
   - User profiles (sellers and buyers)
   - Social features (following, favorites)

3. **Product Catalog Service**
   - Product CRUD operations
   - Image management with CDN
   - Category and attribute management

4. **Search Service**
   - Elasticsearch for product search
   - Advanced filtering and faceting
   - Search analytics and optimization

5. **Order Management Service**
   - Shopping cart functionality
   - Order processing workflow
   - Inventory reservation system

6. **Payment Service**
   - Stripe integration for payments
   - Wallet and refund management
   - Commission calculation

7. **Notification Service**
   - Email notifications (SendGrid)
   - Push notifications (Firebase)
   - SMS alerts for critical updates

## Database Design

### PostgreSQL Schema
- **Users**: artisans, customers, admin users
- **Products**: product catalog with variants
- **Orders**: order lifecycle management
- **Reviews**: customer feedback system

### Redis Cache Strategy
- Session management
- Shopping cart persistence
- Frequently accessed product data
- Search result caching

### File Storage
- **Images**: AWS S3 with CloudFront CDN
- **Documents**: Order receipts, shipping labels
- **Backup**: Automated daily backups

## Security Architecture
- **Authentication**: JWT tokens with refresh rotation
- **API Security**: Rate limiting, CORS, input validation
- **Payment Security**: PCI DSS compliance via Stripe
- **Data Encryption**: TLS 1.3, encrypted database storage

## Performance Requirements
- **Response Time**: <500ms for API calls
- **Search Performance**: <200ms for product searches
- **Image Loading**: <2s for high-res product images
- **Concurrent Users**: Support 10,000+ simultaneous users

## Scalability Strategy
- **Horizontal Scaling**: Auto-scaling groups for all services
- **Database Scaling**: Read replicas + connection pooling
- **CDN Strategy**: Global content distribution
- **Caching Layers**: Multi-level caching (Redis + CDN)

## Technology Stack Summary
- **Frontend**: Next.js, React Native, TypeScript
- **Backend**: Node.js, Express, TypeScript
- **Databases**: PostgreSQL, Redis, Elasticsearch
- **Infrastructure**: AWS/GCP, Kubernetes, Docker
- **Monitoring**: Prometheus, Grafana, Sentry
```

**Human Approval Gate: Architecture Review**
> ✅ User Approved: "Solid architecture! Please prioritize the mobile experience since many artisans use phones to manage their shops."

---

#### Phase 3: Development Implementation (20 minutes)

**🤖 Developer Agent Started**

*Thinking Process:* "I'll create a comprehensive implementation plan with mobile-first approach, focusing on the core MVP features first, then expanding to advanced features."

**Implementation Output:**
```markdown
# Implementation Plan - Handmade Crafts E-Commerce Platform

## Development Phases

### Phase 1: Core MVP (Weeks 1-8)
Foundation services and basic functionality

### Phase 2: Enhanced Features (Weeks 9-12)
Advanced search, social features, mobile optimization

### Phase 3: Scale & Polish (Weeks 13-16)
Performance optimization, analytics, admin tools

## Detailed Implementation

### Frontend Development

#### Web Application Structure
```
src/
├── pages/                 # Next.js pages
│   ├── api/              # API routes
│   ├── shop/             # Shop pages
│   ├── product/          # Product pages
│   └── auth/             # Authentication
├── components/           # Reusable components
│   ├── ui/              # Base UI components
│   ├── product/         # Product-specific
│   ├── cart/            # Shopping cart
│   └── layout/          # Layout components
├── hooks/               # Custom React hooks
├── stores/              # Zustand stores
├── utils/               # Utility functions
└── types/               # TypeScript definitions
```

#### Key Components Implementation

**Product Card Component:**
```typescript
// components/product/ProductCard.tsx
interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
  onAddToWishlist: (productId: string) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onAddToCart,
  onAddToWishlist
}) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  
  return (
    <Card className="group hover:shadow-lg transition-shadow">
      <CardContent className="p-0">
        <div className="relative aspect-square overflow-hidden rounded-t-lg">
          <Image
            src={product.images[currentImageIndex]}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform"
          />
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-2 right-2 bg-white/80"
            onClick={() => onAddToWishlist(product.id)}
          >
            <Heart className="h-4 w-4" />
          </Button>
        </div>
        
        <div className="p-4">
          <h3 className="font-semibold truncate">{product.name}</h3>
          <p className="text-sm text-gray-600 truncate">{product.artisan.name}</p>
          <div className="flex justify-between items-center mt-2">
            <span className="font-bold text-lg">${product.price}</span>
            <Button 
              size="sm" 
              onClick={() => onAddToCart(product)}
              className="bg-craft-primary hover:bg-craft-primary/90"
            >
              Add to Cart
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
```

**Mobile-First Search Component:**
```typescript
// components/search/MobileSearchbar.tsx
export const MobileSearchBar: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<SearchFilters>({});
  const { searchProducts, isLoading } = useProductSearch();
  
  return (
    <div className="sticky top-0 z-10 bg-white border-b p-4">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search handmade crafts..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="icon">
              <Filter className="h-4 w-4" />
            </Button>
          </SheetTrigger>
          <SheetContent side="bottom" className="h-[80vh]">
            <SearchFilters 
              filters={filters} 
              onFiltersChange={setFilters}
            />
          </SheetContent>
        </Sheet>
      </div>
    </div>
  );
};
```

### Backend Implementation

#### API Gateway Setup
```typescript
// services/api-gateway/src/routes.ts
import express from 'express';
import { authenticateToken } from './middleware/auth';
import { rateLimiter } from './middleware/rateLimiter';

const router = express.Router();

// Public routes
router.use('/api/products', rateLimiter, productRoutes);
router.use('/api/search', rateLimiter, searchRoutes);
router.use('/api/auth', authRoutes);

// Protected routes
router.use('/api/cart', authenticateToken, cartRoutes);
router.use('/api/orders', authenticateToken, orderRoutes);
router.use('/api/seller', authenticateToken, sellerRoutes);

export default router;
```

#### Product Catalog Service
```typescript
// services/product-catalog/src/controllers/ProductController.ts
export class ProductController {
  async getProducts(req: Request, res: Response) {
    try {
      const { 
        page = 1, 
        limit = 20, 
        category, 
        priceMin, 
        priceMax,
        sortBy = 'created_at' 
      } = req.query;
      
      const filters = {
        category: category as string,
        price: {
          min: priceMin ? parseFloat(priceMin as string) : undefined,
          max: priceMax ? parseFloat(priceMax as string) : undefined
        }
      };
      
      const products = await this.productService.getProducts({
        page: parseInt(page as string),
        limit: parseInt(limit as string),
        filters,
        sortBy: sortBy as string
      });
      
      res.json({
        data: products.items,
        pagination: products.pagination,
        total: products.total
      });
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch products' });
    }
  }
  
  async createProduct(req: Request, res: Response) {
    try {
      const productData = req.body;
      const sellerId = req.user.id;
      
      // Validate product data
      const validationResult = validateProductData(productData);
      if (!validationResult.valid) {
        return res.status(400).json({ errors: validationResult.errors });
      }
      
      // Process images
      const processedImages = await this.imageService.processProductImages(
        productData.images
      );
      
      const product = await this.productService.createProduct({
        ...productData,
        sellerId,
        images: processedImages
      });
      
      // Index in Elasticsearch for search
      await this.searchService.indexProduct(product);
      
      res.status(201).json(product);
    } catch (error) {
      res.status(500).json({ error: 'Failed to create product' });
    }
  }
}
```

#### Search Service Integration
```typescript
// services/search/src/SearchService.ts
import { Client } from '@elastic/elasticsearch';

export class SearchService {
  private client: Client;
  
  constructor() {
    this.client = new Client({
      node: process.env.ELASTICSEARCH_URL,
      auth: {
        username: process.env.ELASTICSEARCH_USERNAME,
        password: process.env.ELASTICSEARCH_PASSWORD
      }
    });
  }
  
  async searchProducts(query: string, filters: SearchFilters) {
    const searchBody = {
      query: {
        bool: {
          must: [
            {
              multi_match: {
                query,
                fields: ['name^3', 'description^2', 'tags', 'artisan.name'],
                type: 'best_fields',
                fuzziness: 'AUTO'
              }
            }
          ],
          filter: this.buildFilters(filters)
        }
      },
      sort: this.buildSort(filters.sortBy),
      from: (filters.page - 1) * filters.limit,
      size: filters.limit,
      aggs: {
        categories: {
          terms: { field: 'category.keyword' }
        },
        price_ranges: {
          range: {
            field: 'price',
            ranges: [
              { to: 25 },
              { from: 25, to: 50 },
              { from: 50, to: 100 },
              { from: 100 }
            ]
          }
        }
      }
    };
    
    const response = await this.client.search({
      index: 'products',
      body: searchBody
    });
    
    return {
      products: response.body.hits.hits.map(hit => hit._source),
      total: response.body.hits.total.value,
      aggregations: response.body.aggregations
    };
  }
  
  private buildFilters(filters: SearchFilters) {
    const filterClauses = [];
    
    if (filters.category) {
      filterClauses.push({ term: { 'category.keyword': filters.category } });
    }
    
    if (filters.priceMin || filters.priceMax) {
      const priceRange: any = {};
      if (filters.priceMin) priceRange.gte = filters.priceMin;
      if (filters.priceMax) priceRange.lte = filters.priceMax;
      filterClauses.push({ range: { price: priceRange } });
    }
    
    if (filters.inStock) {
      filterClauses.push({ range: { inventory_count: { gt: 0 } } });
    }
    
    return filterClauses;
  }
}
```

### Mobile App Implementation

#### React Native Core Structure
```typescript
// mobile/src/navigation/AppNavigator.tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

export const AppNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          if (route.name === 'Home') iconName = 'home';
          else if (route.name === 'Search') iconName = 'search';
          else if (route.name === 'Cart') iconName = 'shopping-cart';
          else if (route.name === 'Profile') iconName = 'user';
          
          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#8B5CF6',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Home" component={HomeStack} />
      <Tab.Screen name="Search" component={SearchStack} />
      <Tab.Screen name="Cart" component={CartStack} />
      <Tab.Screen name="Profile" component={ProfileStack} />
    </Tab.Navigator>
  );
};
```

### Database Schema Implementation
```sql
-- Core database schema
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('buyer', 'seller', 'admin')),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    profile_image_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE artisan_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    shop_name VARCHAR(255) NOT NULL,
    bio TEXT,
    location VARCHAR(255),
    specialties TEXT[],
    verified BOOLEAN DEFAULT FALSE,
    commission_rate DECIMAL(5,4) DEFAULT 0.08,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artisan_id UUID REFERENCES artisan_profiles(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id UUID REFERENCES categories(id),
    tags TEXT[],
    images JSONB NOT NULL,
    dimensions JSONB,
    materials TEXT[],
    inventory_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'sold')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id UUID REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
    shipping_address JSONB NOT NULL,
    payment_intent_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_artisan ON products(artisan_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_orders_buyer ON orders(buyer_id);
CREATE INDEX idx_orders_status ON orders(status);
```

### Deployment Configuration
```yaml
# kubernetes/production/e-commerce-platform.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-catalog-service
  namespace: e-commerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-catalog
  template:
    metadata:
      labels:
        app: product-catalog
    spec:
      containers:
      - name: product-catalog
        image: ecommerce/product-catalog:v1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Testing Strategy
```typescript
// tests/integration/product.test.ts
describe('Product Management Integration', () => {
  test('Create product workflow', async () => {
    // 1. Authenticate as seller
    const sellerToken = await authenticate('seller@test.com', 'password');
    
    // 2. Upload product images
    const imageUrls = await uploadImages(['craft1.jpg', 'craft2.jpg']);
    
    // 3. Create product
    const productData = {
      name: 'Handwoven Scarf',
      description: 'Beautiful handwoven scarf made from organic cotton',
      price: 45.00,
      category: 'accessories',
      tags: ['handwoven', 'organic', 'scarf'],
      images: imageUrls,
      inventory_count: 5
    };
    
    const response = await request(app)
      .post('/api/products')
      .set('Authorization', `Bearer ${sellerToken}`)
      .send(productData)
      .expect(201);
    
    // 4. Verify product is searchable
    const searchResponse = await request(app)
      .get('/api/search?q=handwoven')
      .expect(200);
    
    expect(searchResponse.body.products).toContain(
      expect.objectContaining({ name: 'Handwoven Scarf' })
    );
  });
});
```
```

---

#### Phase 4: Quality Assurance (15 minutes)

**🤖 QA Tester Agent Started**

*Thinking Process:* "I need to create a comprehensive testing strategy for this e-commerce platform, focusing on mobile experience, payment security, and user workflows."

**QA Testing Output:**
```markdown
# Quality Assurance Plan - Handmade Crafts E-Commerce Platform

## Testing Strategy Overview

### Testing Pyramid
1. **Unit Tests (70%)**: Individual component and service testing
2. **Integration Tests (20%)**: Service-to-service communication
3. **E2E Tests (10%)**: Critical user journeys

### Test Environments
- **Development**: Continuous testing during development
- **Staging**: Pre-production testing with production-like data
- **Production**: Monitoring and smoke tests

## Critical Test Scenarios

### 1. User Registration & Authentication
**Test Cases:**
- Seller registration with shop setup
- Buyer registration with social login
- Password reset and security
- Multi-factor authentication for sellers

**Mobile-Specific Tests:**
- Biometric authentication (fingerprint/face)
- App backgrounding during auth flow
- Push notification permissions

### 2. Product Management Workflow
**Seller Journey Tests:**
```gherkin
Feature: Product Management
  Scenario: Seller creates new product
    Given I am logged in as a verified seller
    When I navigate to "Add Product"
    And I upload 5 high-quality images
    And I fill in product details:
      | Field       | Value                    |
      | Name        | Ceramic Coffee Mug       |
      | Price       | 28.00                   |
      | Category    | Kitchen & Dining        |
      | Description | Hand-thrown ceramic mug |
    And I set inventory to 10 items
    And I click "Publish Product"
    Then I should see "Product published successfully"
    And the product should appear in my shop
    And the product should be searchable
```

**Automated Test Implementation:**
```typescript
// e2e/tests/product-creation.spec.ts
import { test, expect } from '@playwright/test';

test('Seller can create and publish product', async ({ page, context }) => {
  // Login as seller
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'seller@test.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-button"]');
  
  // Navigate to add product
  await page.click('[data-testid="add-product-button"]');
  
  // Upload images
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles([
    'tests/fixtures/mug1.jpg',
    'tests/fixtures/mug2.jpg'
  ]);
  
  // Fill product form
  await page.fill('[data-testid="product-name"]', 'Ceramic Coffee Mug');
  await page.fill('[data-testid="product-price"]', '28.00');
  await page.selectOption('[data-testid="product-category"]', 'kitchen-dining');
  await page.fill('[data-testid="product-description"]', 'Hand-thrown ceramic mug');
  await page.fill('[data-testid="inventory-count"]', '10');
  
  // Publish product
  await page.click('[data-testid="publish-button"]');
  
  // Verify success
  await expect(page.locator('[data-testid="success-message"]')).toContainText('Product published successfully');
  
  // Verify product appears in search
  await page.goto('/search?q=ceramic+mug');
  await expect(page.locator('[data-testid="product-card"]')).toContainText('Ceramic Coffee Mug');
});
```

### 3. Shopping Cart & Checkout Flow
**Critical E2E Test:**
```typescript
test('Complete purchase flow', async ({ page, context }) => {
  // Add multiple items to cart
  await page.goto('/product/ceramic-mug-123');
  await page.click('[data-testid="add-to-cart"]');
  
  await page.goto('/product/handwoven-scarf-456');
  await page.selectOption('[data-testid="size-select"]', 'medium');
  await page.click('[data-testid="add-to-cart"]');
  
  // Review cart
  await page.click('[data-testid="cart-icon"]');
  await expect(page.locator('[data-testid="cart-items"]')).toHaveCount(2);
  
  // Proceed to checkout
  await page.click('[data-testid="checkout-button"]');
  
  // Fill shipping information
  await page.fill('[data-testid="first-name"]', 'John');
  await page.fill('[data-testid="last-name"]', 'Doe');
  await page.fill('[data-testid="address"]', '123 Main St');
  await page.fill('[data-testid="city"]', 'San Francisco');
  await page.fill('[data-testid="zip"]', '94102');
  
  // Payment (using Stripe test mode)
  await page.frameLocator('[data-testid="stripe-frame"]').fill('[data-testid="card-number"]', '4242424242424242');
  await page.frameLocator('[data-testid="stripe-frame"]').fill('[data-testid="card-expiry"]', '12/25');
  await page.frameLocator('[data-testid="stripe-frame"]').fill('[data-testid="card-cvc"]', '123');
  
  // Complete purchase
  await page.click('[data-testid="place-order-button"]');
  
  // Verify order confirmation
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible();
  const orderNumber = await page.locator('[data-testid="order-number"]').textContent();
  expect(orderNumber).toMatch(/ORDER-\d+/);
});
```

### 4. Mobile App Testing
**React Native Testing with Detox:**
```typescript
// mobile/e2e/search-and-purchase.e2e.js
describe('Mobile Search and Purchase Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('should search for products and add to cart', async () => {
    // Search for products
    await element(by.id('search-input')).tap();
    await element(by.id('search-input')).typeText('ceramic mug');
    await element(by.id('search-button')).tap();
    
    // Verify search results
    await expect(element(by.id('product-list'))).toBeVisible();
    await expect(element(by.text('Ceramic Coffee Mug'))).toBeVisible();
    
    // Tap on first product
    await element(by.id('product-card-0')).tap();
    
    // Add to cart
    await element(by.id('add-to-cart-button')).tap();
    
    // Verify cart badge updates
    await expect(element(by.id('cart-badge'))).toHaveText('1');
  });
  
  it('should handle offline mode gracefully', async () => {
    // Simulate network disconnection
    await device.setNetworkState('disconnected');
    
    // Try to browse products
    await element(by.id('home-tab')).tap();
    
    // Should show cached products
    await expect(element(by.id('offline-banner'))).toBeVisible();
    await expect(element(by.id('product-list'))).toBeVisible();
    
    // Try to add to cart (should queue for later)
    await element(by.id('product-card-0')).tap();
    await element(by.id('add-to-cart-button')).tap();
    await expect(element(by.text('Added to cart (will sync when online)'))).toBeVisible();
    
    // Restore network
    await device.setNetworkState('connected');
    
    // Verify sync occurs
    await waitFor(element(by.id('offline-banner'))).not.toBeVisible().withTimeout(5000);
  });
});
```

### 5. Performance Testing
**Load Testing with Artillery:**
```yaml
# performance/load-test.yml
config:
  target: 'https://api.handmade-crafts.com'
  phases:
    - duration: 300
      arrivalRate: 10
      name: "Warm up"
    - duration: 600
      arrivalRate: 50
      name: "Peak traffic"
    - duration: 300
      arrivalRate: 100
      name: "Stress test"
  defaults:
    headers:
      Content-Type: 'application/json'

scenarios:
  - name: "Browse and search products"
    weight: 60
    flow:
      - get:
          url: "/api/products"
      - get:
          url: "/api/search?q=handmade"
      - get:
          url: "/api/products/{{ $randomUUID }}"
  
  - name: "User authentication"
    weight: 20
    flow:
      - post:
          url: "/api/auth/login"
          json:
            email: "user{{ $randomInt(1, 1000) }}@test.com"
            password: "password123"
  
  - name: "Add to cart and checkout"
    weight: 20
    flow:
      - post:
          url: "/api/cart/add"
          json:
            productId: "{{ $randomUUID }}"
            quantity: 1
      - get:
          url: "/api/cart"
      - post:
          url: "/api/orders"
          json:
            paymentMethodId: "pm_test_card"
```

### 6. Security Testing
**OWASP Security Tests:**
```typescript
// security/api-security.test.ts
describe('API Security Tests', () => {
  test('SQL Injection Protection', async () => {
    const maliciousQuery = "'; DROP TABLE products; --";
    
    const response = await request(app)
      .get(`/api/search?q=${encodeURIComponent(maliciousQuery)}`)
      .expect(400);
    
    expect(response.body.error).toContain('Invalid search query');
  });
  
  test('Rate Limiting', async () => {
    const requests = Array(101).fill().map(() => 
      request(app).get('/api/products')
    );
    
    const responses = await Promise.all(requests);
    const rateLimitedResponses = responses.filter(r => r.status === 429);
    
    expect(rateLimitedResponses.length).toBeGreaterThan(0);
  });
  
  test('Authentication Required', async () => {
    await request(app)
      .post('/api/products')
      .send({ name: 'Test Product' })
      .expect(401);
  });
  
  test('XSS Protection', async () => {
    const xssPayload = '<script>alert("xss")</script>';
    
    const response = await request(app)
      .post('/api/products')
      .set('Authorization', `Bearer ${sellerToken}`)
      .send({
        name: xssPayload,
        description: 'Test product',
        price: 100
      })
      .expect(400);
    
    expect(response.body.errors).toContain('Invalid characters in product name');
  });
});
```

## Quality Metrics Dashboard

### Test Coverage Requirements
- **Backend Services**: 90%+ code coverage
- **Frontend Components**: 85%+ coverage
- **Mobile App**: 80%+ coverage
- **Critical Paths**: 100% E2E test coverage

### Performance Benchmarks
- **Page Load Time**: <2 seconds (95th percentile)
- **API Response Time**: <500ms (average)
- **Search Performance**: <200ms (average)
- **Mobile App Startup**: <3 seconds

### Browser/Device Support Matrix
| Browser/Device | Versions | Priority |
|---------------|----------|----------|
| Chrome        | Latest 2 | High     |
| Safari        | Latest 2 | High     |
| Firefox       | Latest 2 | Medium   |
| Edge          | Latest 2 | Medium   |
| iOS Safari    | iOS 15+  | High     |
| Android Chrome| Android 10+ | High  |

### Accessibility Testing
- **WCAG 2.1 AA Compliance**: 100%
- **Screen Reader Compatibility**: NVDA, JAWS, VoiceOver
- **Keyboard Navigation**: All interactions accessible
- **Color Contrast**: 4.5:1 minimum ratio
```

**Final Quality Report:**
- ✅ 127 automated tests passing
- ✅ 92% code coverage achieved
- ✅ Performance benchmarks met
- ✅ Security vulnerabilities addressed
- ✅ Mobile responsiveness validated
- ✅ Accessibility compliance verified

---

## Workflow Completion Summary

### Total Execution Time: 55 minutes
### Success Metrics:
- **Requirement Completeness**: 98% of user requirements addressed
- **Technical Feasibility**: 95% confidence in implementation approach
- **Quality Score**: 9.2/10 based on automated validation
- **Cost Estimate**: $85k-120k development cost, $3k-8k/month operational

### Deliverables Created:
1. **Business Requirements Document** (8 pages)
2. **Technical Architecture Specification** (12 pages)
3. **Complete Implementation Plan** (20 pages)
4. **Quality Assurance Strategy** (15 pages)
5. **Mobile App Specifications** (6 pages)
6. **Database Schema & API Documentation** (10 pages)

### Next Steps Recommended:
1. **Week 1-2**: Set up development environment and CI/CD
2. **Week 3-4**: Implement core backend services
3. **Week 5-6**: Build web frontend MVP
4. **Week 7-8**: Develop mobile app MVP
5. **Week 9-12**: Integration testing and optimization
6. **Week 13-16**: Production deployment and monitoring

---

## Example 2: Marketing Campaign Development

### User Input
> "We need a comprehensive marketing campaign for our new sustainable sneaker line targeting Gen Z consumers. Budget is $500k over 6 months."

### Intent Classification & Workflow Assembly

**Detected Domain**: `marketing_campaign`  
**Complexity**: `complex`  
**Selected Agents**: Market Researcher → Campaign Strategist → Creative Director → Media Planner

### Abbreviated Workflow Execution

#### Market Researcher Output (10 minutes):
```markdown
# Market Research - Sustainable Sneakers for Gen Z

## Target Audience Analysis
- **Primary**: Ages 18-26, urban/suburban, college-educated
- **Values**: Environmental consciousness, authenticity, social justice
- **Shopping Behavior**: 78% research online before purchase
- **Influence Sources**: TikTok (67%), Instagram (45%), YouTube (38%)

## Competitive Landscape
- **Direct Competitors**: Allbirds, Veja, Rothy's
- **Market Gap**: Affordable sustainable options under $150
- **Pricing Strategy**: Recommend $89-129 price point

## Campaign Insights
- **Seasonal Timing**: Launch in March for spring/summer season
- **Key Messages**: "Style meets sustainability", "Walk your values"
- **Channel Priorities**: Social-first strategy with influencer partnerships
```

#### Campaign Strategist Output (12 minutes):
```markdown
# Campaign Strategy - Sustainable Sneaker Launch

## Campaign Overview
- **Objective**: Generate 25k units sold in 6 months
- **Budget Allocation**: $300k media, $150k influencers, $50k content
- **Timeline**: 2-month pre-launch, 4-month active campaign

## Strategic Framework
1. **Awareness Phase** (Months 1-2): Brand introduction via influencers
2. **Consideration Phase** (Months 3-4): Product demonstrations and reviews  
3. **Conversion Phase** (Months 5-6): Limited-time offers and social proof

## Channel Strategy
- **TikTok** (40% budget): Viral sustainability challenges
- **Instagram** (30% budget): Lifestyle and product photography
- **YouTube** (20% budget): Behind-the-scenes manufacturing content
- **Influencer Partnerships** (10% budget): Micro and macro influencers
```

#### Creative Director Output (15 minutes):
```markdown
# Creative Campaign - "Step Forward, Step Green"

## Visual Identity
- **Color Palette**: Earth tones with vibrant accent colors
- **Typography**: Modern, clean sans-serif fonts
- **Photography Style**: Natural lighting, authentic moments

## Content Pillars
1. **Sustainability Story**: Manufacturing process transparency
2. **Style Versatility**: Multiple outfit combinations
3. **Community Impact**: Environmental initiatives supported

## Asset Requirements
- 50+ product photography shots
- 12 video advertisements (15-60 seconds)
- Social media template library
- Influencer content guidelines

## Campaign Taglines
- Primary: "Step Forward, Step Green"
- Secondary: "Where Style Meets Sustainability"
- CTA: "Walk Your Values"
```

#### Media Planner Output (8 minutes):
```markdown
# Media Plan - 6-Month Campaign Execution

## Budget Allocation by Channel
- **TikTok Ads**: $200k (CPM: $8-12)
- **Instagram/Facebook**: $150k (CPM: $10-15)  
- **YouTube**: $100k (CPV: $0.05-0.08)
- **Google Ads**: $50k (CPC: $1.50-3.00)

## Targeting Strategy
- **Demographics**: Ages 18-26, household income $40k+
- **Interests**: Sustainability, fashion, outdoor activities
- **Behaviors**: Eco-conscious shoppers, social media active

## Campaign Calendar
- **Pre-Launch** (Feb-Mar): Teaser content, influencer seeding
- **Launch** (Apr-May): Full campaign activation
- **Optimization** (Jun-Jul): Performance-based budget reallocation

## Success Metrics
- **Awareness**: 5M+ impressions, 2% engagement rate
- **Consideration**: 100k+ website visits, 15% email signups
- **Conversion**: 25k units sold, $2.2M revenue target
```

### Campaign Results Projection:
- **ROI**: 340% expected return on ad spend
- **Brand Awareness**: 23% lift in target demographic
- **Sales Impact**: 25,000 units projected
- **Customer Acquisition Cost**: $20 average

---

This comprehensive workflow example demonstrates how the MCP-based agent orchestration system can handle complex, multi-faceted projects by leveraging specialized agents that work together seamlessly while maintaining their domain expertise and constraints.