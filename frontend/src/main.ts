import { CommonModule } from '@angular/common';
import { HttpClient, provideHttpClient } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { bootstrapApplication } from '@angular/platform-browser';

type Mode = 'discrete' | 'continuous';

interface ConvertResponse {
  original: string;
  mode: Mode;
  semantic_concepts: string[];
  semantic_flags: Record<string, boolean>;
  semantic_code: number[];
  recovered: string;
  code_bits: number;
  metrics: Record<string, number | boolean>;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app/app.html',
  styleUrl: './app/app.scss'
})
class AppComponent {
  private readonly http = inject(HttpClient);

  private readonly apiBaseUrl = 'https://text-semantic-codec-api.onrender.com';
  inputText = 'The meeting has been postponed because of the heavy rain.';
  mode: Mode = 'discrete';
  codebookSize = 256;
  semanticTokens = 4;
  dimensions = 16;

  result = signal<ConvertResponse | null>(null);
  loading = signal(false);
  error = signal('');

  compressionPercent = computed(() => {
    const value = this.result()?.metrics['compression_ratio'];
    return typeof value === 'number' ? `${(value * 100).toFixed(2)}%` : 'n/a';
  });

  similarityPercent = computed(() => {
    const value = this.result()?.metrics['sentence_similarity'];
    return typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : 'n/a';
  });

  convert(): void {
    const text = this.inputText.trim();
    if (!text) {
      this.error.set('Please enter text to convert.');
      return;
    }

    this.loading.set(true);
    this.error.set('');
    this.result.set(null);

    const endpoint = `${this.apiBaseUrl.replace(/\/$/, '')}/api/semantic/convert`;
    this.http.post<ConvertResponse>(endpoint, {
      text,
      mode: this.mode,
      codebook_size: this.codebookSize,
      semantic_tokens: this.semanticTokens,
      dimensions: this.dimensions
    }).subscribe({
      next: (response) => {
        this.result.set(response);
        this.loading.set(false);
      },
      error: (err) => {
        const detail = err?.error?.detail;
        this.error.set(typeof detail === 'string' ? detail : 'Unable to reach the semantic codec API.');
        this.loading.set(false);
      }
    });
  }
}

bootstrapApplication(AppComponent, {
  providers: [provideHttpClient()]
}).catch((error) => console.error(error));
