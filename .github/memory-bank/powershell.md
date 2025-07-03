## PowerShell command rules
- When showing a PowerShell command that calls a full-path executable, **always**
  prefix the quoted path with an ampersand (`&`).
- Pattern:  
  & "C:/absolute/path/to/exe.exe" <args>
- Never omit the `&` or the double quotes.