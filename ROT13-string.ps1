function rot13-string {
<# 
.SYNOPSIS
The purpose of this function is to be able to perform ROT13 letter shifts.This function can rotate the ASCII table or the alphabet. When you do the alphabet it will convert everything to lowercase
and then rotate letters. If you do the ASCII table it will rotate by character. This works by converting the character to it's 
decimal number then adding the rotate followed by modulus to perform the key shift.
 
.DESCRIPTION
__________ _______________________________                     __         .__                
\______   \\_____  \__    ___/_   \_____  \            _______/  |________|__| ____    ____  
 |       _/ /   |   \|    |   |   | _(__  <   ______  /  ___/\   __\_  __ \  |/    \  / ___\ 
 |    |   \/    |    \    |   |   |/       \ /_____/  \___ \  |  |  |  | \/  |   |  \/ /_/  >
 |____|_  /\_______  /____|   |___/______  /         /____  > |__|  |__|  |__|___|  /\___  / 
        \/         \/                    \/               \/                      \//_____/  

.EXAMPLE
  
rot13-string -type ASCII -string abcdefghijklmnopqrstuvwxyz -rotate 13
rot13-string -type Alaphabet -string abcdefghijklmnopqrstuvwxyz -rotate 13

#>

[cmdletbinding()]
param (
[validateSet("ASCII","Alaphabet")]
[string]$type,
[string]$string,
[int]$rotate)

# This is for ASCII
if ( $type -eq "ASCII" ){
$length = $string.length - 1
$convertedstring = $string.ToCharArray() | %{[int][char]$_}
[string]$rotatedword = ''
foreach ( $i in 0..$length) { 

$modulus = ($convertedstring[$i]+$rotate) % 127
if ( $modulus -lt 32  ) { 
$value = $modulus + 32     
$letter = [char]$value
$rotatedword = $rotatedword + $letter
Remove-Variable -Name letter
} 
else {
$value = $modulus
$letter = [char]$value
$rotatedword = $rotatedword + $letter
}
} 
}
else {

# Now doing just the alphabet
$string = $string.ToLower()
$length = $string.length - 1
$convertedstring = $string.ToCharArray() | %{[int][char]$_}
[string]$rotatedword = ''
foreach ( $i in 0..$length) {

$modulus = ($convertedstring[$i]+$rotate) % 123
if ( $modulus -lt 97  ) { 
$value = $modulus + 97
$letter = [char]$value
$rotatedword = $rotatedword + $letter
Remove-Variable -Name letter
} 
else {
$value = $modulus
$letter = [char]$value
$rotatedword = $rotatedword + $letter
}
}
}
return $rotatedword
}


