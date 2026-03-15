using System.ComponentModel;
using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.JSInterop;

namespace ContabilidadPanama.Frontend.Services;

public class AuthService : INotifyPropertyChanged
{
    private readonly IJSRuntime _js;
    private readonly HttpClient _http;
    private bool _isAuthenticated;
    private string _token = "";
    private string _baseUrl = "https://app.contapanama.rsanjur.com/api";
    
    public event PropertyChangedEventHandler? PropertyChanged;
    
    public bool IsAuthenticated 
    { 
        get => _isAuthenticated;
        private set 
        {
            if (_isAuthenticated != value)
            {
                _isAuthenticated = value;
                OnPropertyChanged(nameof(IsAuthenticated));
            }
        }
    }

    public string Token 
    { 
        get => _token;
        private set 
        {
            _token = value;
            OnPropertyChanged(nameof(Token));
        }
    }

    public AuthService(IJSRuntime js, HttpClient http)
    {
        _js = js;
        _http = http;
    }

    public async Task CheckAuthAsync()
    {
        try
        {
            var token = await _js.InvokeAsync<string>("localStorage.getItem", "auth_token");
            if (!string.IsNullOrEmpty(token))
            {
                _token = token;
                _isAuthenticated = true;
            }
            else
            {
                _token = "";
                _isAuthenticated = false;
            }
        }
        catch
        {
            _isAuthenticated = false;
            _token = "";
        }
        OnPropertyChanged(nameof(IsAuthenticated));
        OnPropertyChanged(nameof(Token));
    }

    public async Task<(bool Success, string? Error)> LoginAsync(string email, string password)
    {
        try
        {
            var response = await _http.PostAsJsonAsync($"{_baseUrl}/auth/login", new 
            {
                email = email,
                password = password
            });

            if (response.IsSuccessStatusCode)
            {
                Console.WriteLine($"Login response status: {response.StatusCode}");
                var result = await response.Content.ReadFromJsonAsync<LoginResponse>();
                Console.WriteLine($"Login result: {result?.AccessToken}");
                if (result != null && !string.IsNullOrEmpty(result.AccessToken))
                {
                    await _js.InvokeVoidAsync("localStorage.setItem", "auth_token", result.AccessToken);
                    _token = result.AccessToken;
                    _isAuthenticated = true;
                    OnPropertyChanged(nameof(IsAuthenticated));
                    OnPropertyChanged(nameof(Token));
                    return (true, null);
                }
                return (false, "Respuesta inválida del servidor");
            }
            else
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Login failed: {response.StatusCode} - {errorContent}");
                
                // Intentar parsear el error del backend
                try
                {
                    var errorObj = System.Text.Json.JsonSerializer.Deserialize<ErrorResponse>(errorContent);
                    if (!string.IsNullOrEmpty(errorObj?.detail))
                    {
                        return (false, errorObj.detail);
                    }
                }
                catch { }
                
                return (false, "Email o contraseña incorrectos");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Login error: {ex.Message}");
            return (false, $"Error de conexión: {ex.Message}");
        }
    }

    public async Task LogoutAsync()
    {
        await _js.InvokeVoidAsync("localStorage.removeItem", "auth_token");
        _token = "";
        _isAuthenticated = false;
        OnPropertyChanged(nameof(IsAuthenticated));
        OnPropertyChanged(nameof(Token));
    }

    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private class LoginResponse
    {
        [JsonPropertyName("access_token")]
        public string? AccessToken { get; set; }
        [JsonPropertyName("token_type")]
        public string? TokenType { get; set; }
    }

    private class ErrorResponse
    {
        public string? detail { get; set; }
    }
}
