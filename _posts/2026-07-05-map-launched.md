---
layout: post
title: "Map launched"
description: "KDC's dataset is now a browsable map."
---

KDC now has a [map](/map/). Every tracked project-site plots as a
status-coloured marker — clustered, and filterable by status, operator, and
state — over an OpenStreetMap basemap. Per-record pages gain a locator map.

The map is static and privacy-clean: points are pre-rendered from the records
into committed GeoJSON (no runtime service, no API key), and it is progressive
enhancement over the existing tables — with JavaScript off, the tables are
still the record. Markers are approximate, geocoded from each record's sourced
location; exact parcel geometry is a later layer. See
[coverage](/coverage/#geo-completeness) for precision and completeness.
