### Credentials setting

```bash
export GOOGLE_APPLICATION_CREDENTIALS="ecommerce-dev-392819-dde10994963d.json"
```

## Presentation to GCR deployment.

Dev

```bash
python ci/presentation.py --gcp_project_id "ecommerce-dev-392819"
```

Prod

```bash
python ci/presentation.py --gcp_project_id "xxxx"
```

