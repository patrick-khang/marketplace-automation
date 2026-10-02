# Marketplace Automation

A reconstruction of an internal marketplace automation project I developed for Tofu TCG, an e-commerce trading-card business.

## Background

Managing collectible inventory across online marketplaces involved repetitive data entry, frequent inventory changes, and changing market prices. Manual entry also created opportunities for inconsistent product information and listing errors.

I developed a Python-based workflow to retrieve product metadata from external APIs, structure marketplace listing data, process inventory records, validate listings, and interact with eBay's APIs.

Portions of the original workflow were successfully used to create real marketplace listings. Other components, including broader inventory synchronization and market monitoring, remained experimental.

## Original Workflow

The project evolved into a multi-step workflow for turning physical trading-card inventory into structured marketplace listings.

```text
Card Images
    ↓
Google Cloud Storage
    ↓
image_inventory_ingestion.py
    ↓
Structured Inventory CSV
    ↓
product_lookup.py
    ↓
External Product Metadata
    ↓
batch_listing.py
    ↓
Construct eBay Listing
    ↓
verify_and_submit.py
    ↓
Verify → Submit to eBay
```

## Historical Implementation

The `historical/` directory contains sanitized components from the original implementation.

### `product_lookup.py`

Queries an external trading-card API and matches product information using card name, set code, and rarity. The returned data is normalized for use by the marketplace workflow.

### `image_inventory_ingestion.py`

Retrieves inventory images from Google Cloud Storage and derives structured inventory records from image filenames. The resulting records are written to CSV for downstream processing.

### `batch_listing.py`

Reads inventory records from CSV, enriches them with external product metadata, constructs eBay listing payloads, and submits fixed-price listings through the eBay Trading API.

### `verify_and_submit.py`

Demonstrates a validation step added during development. Listing payloads are verified with eBay before the actual listing operation is allowed to proceed.

## What Worked

- Retrieved and normalized product metadata from an external REST API
- Used cloud-hosted inventory images as part of the listing workflow
- Converted inventory information into structured CSV records
- Constructed marketplace listing payloads programmatically
- Processed multiple inventory records through a batch workflow
- Successfully used portions of the workflow to create real marketplace listings
- Added API verification before performing a listing operation

## Limitations of the Original Design

The project grew incrementally while I was learning to work with external APIs, so the implementation contains several design decisions I would approach differently today.

Examples include:

- API access, business logic, and listing construction were tightly coupled
- Missing values sometimes used unsafe operational defaults
- Configuration management was inconsistent
- Some marketplace identifiers were hardcoded
- Filename conventions were used as a lightweight inventory schema
- Error handling relied heavily on console output
- Several experimental implementations duplicated similar logic

## What I Would Change Today

I would separate the system into explicit components for:

- authentication and configuration
- external API clients
- inventory persistence
- product-data normalization
- listing construction
- validation
- marketplace operations
- logging and error handling

I would also validate required inventory fields before allowing any marketplace operation, use structured configuration rather than hardcoded values, and add automated tests around data transformation and listing validation.

## Project Status

This repository is a reconstruction of an internal automation project rather than a production application.

The historical code has been sanitized to remove credentials, account-specific identifiers, and unrelated experimental material. It is included to demonstrate the original technical problem, implementation process, and lessons learned from building the system.
