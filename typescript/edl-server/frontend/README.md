# Pomegranate EDL Manager

A modern Angular application for managing Palo Alto Networks External Dynamic Lists (EDLs). This project is built using Angular 19 and the Sakai-NG admin template.

## Project Overview

Pomegranate EDL Manager provides a web interface for performing CRUD operations on Palo Alto Networks EDLs (External Dynamic Lists). The application allows users to:

- View EDL status and statistics
- Manage IP blocklists
- Manage domain blocklists
- Manage URL blocklists
- Handle custom lists

## Technical Stack

- Angular 19
- Standalone Components
- New Angular Control Flow (@if, @else)
- PrimeNG UI Components
- TailwindCSS
- Sakai-NG Admin Template

## Prerequisites

- Node.js (v18 or higher)
- npm (v9 or higher)
- Angular CLI

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd pomegranate
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
ng serve
```

4. Navigate to `http://localhost:4200/` in your browser.

## Project Structure

The application follows a strict component structure:
```
{component_name}/
├── {component_name}.scss
├── {component_name}.html
└── {component_name}.ts
```

## Development Notes

- The application uses Angular's new control flow syntax (@if, @else)
- @ngIf and @ngClass are not used in favor of the new syntax
- All components are standalone
- Component templates must be in separate .html files

## Features

- Dashboard with EDL status overview
- Real-time EDL statistics
- CRUD operations for lists
- Dark/Light theme support
- Responsive design

## Building for Production

To build the application for production:

```bash
ng build --configuration production
```

The build artifacts will be stored in the `dist/` directory.
