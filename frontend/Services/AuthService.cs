using System.Net.Http.Json;
using Microsoft.JSInterop;

namespace ContabilidadPanama.Frontend.Services;

public class AuthService
{
    private readonly HttpClient _httpClient;
    private readonly IJSRuntime _jsRuntime;
    private const string TokenKey = "auth_token";
    
    public event Action? AuthStateChanged;
    public UserInfo? CurrentUser { get; private set; }
    
    public AuthService(HttpClient httpClient, IJSRuntime jsRuntime)
    {
        _httpClient = httpClient;
        _jsRuntime = jsRuntime;
    }
    
    public async Task<(bool Success, string? Error)> LoginAsync(string email, string password)
    {
        try
        {
            var loginData = new { email, password };
            var response = await _httpClient.PostAsJsonAsync("http://localhost:8000/api/auth/login", loginData);
            
            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadFromJsonAsync<LoginResponse>();
                if (result != null)
                {
                    await _jsRuntime.InvokeVoidAsync("localStorage.setItem", TokenKey, result.access_token);
                    await _jsRuntime.InvokeVoidAsync("localStorage.setItem", "auth_user", System.Text.Json.JsonSerializer.Serialize(result.user));
                    CurrentUser = result.user;
                    AuthStateChanged?.Invoke();
                    return (true, null);
                }
            }
            
            return (false, "Credenciales inválidas");
        }
        catch (Exception ex)
        {
            return (false, $"Error de conexión: {ex.Message}");
        }
    }
    
    public async Task LogoutAsync()
    {
        await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", TokenKey);
        await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", "auth_user");
        CurrentUser = null;
        AuthStateChanged?.Invoke();
    }
    
    public async Task<string?> GetTokenAsync()
    {
        return await _jsRuntime.InvokeAsync<string>("localStorage.getItem", TokenKey);
    }
    
    public async Task<bool> IsAuthenticatedAsync()
    {
        var token = await GetTokenAsync();
        return !string.IsNullOrEmpty(token);
    }
    
    public async Task<UserInfo?> GetCurrentUserAsync()
    {
        if (CurrentUser != null) return CurrentUser;
        
        var userJson = await _jsRuntime.InvokeAsync<string>("localStorage.getItem", "auth_user");
        if (!string.IsNullOrEmpty(userJson))
        {
            CurrentUser = System.Text.Json.JsonSerializer.Deserialize<UserInfo>(userJson);
        }
        return CurrentUser;
    }
}

public class LoginResponse
{
    public string access_token { get; set; } = "";
    public string token_type { get; set; } = "bearer";
    public UserInfo user { get; set; } = new();
}

public class UserInfo
{
    public int id { get; set; }
    public string email { get; set; } = "";
    public string name { get; set; } = "";
    public int tenant_id { get; set; }
    public string role { get; set; } = "";
    public bool is_active { get; set; }
}
