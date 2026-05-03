{{/* Etiquetas comunes */}}
{{- define "automex.labels" -}}
app.kubernetes.io/name: {{ .name }}
app.kubernetes.io/managed-by: helm
proyecto: automex
{{- end -}}
