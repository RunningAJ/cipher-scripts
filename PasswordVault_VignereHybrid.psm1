####################################################################
# Text File Encrypter  
# Date 28JUL2017 
# Version 0.4.5.Module3 agghhh shit save as... rename 
# IF I COULD GO BACK AND WRITE IT ALL OVER AGAIN...
# I WOULD. BUT I DON'T HAVE THAT TYPE OF TIME SO I'VE MOVED ON.                               
####################################################################
# This is a module that will create a password keeper in powershell 
# This uses a hybrid Vigenere cipher by converting your password
# to a SHA256 hash. Instead of using a standard dictionary for the
# letter rotation, I take the pin you entered in to run a sub 
# vigenere routine which then outputs a custom char array character
# rotation. From there I take the SHA256 hash and use that as the
# key to encrypt the plain text while using that custom char array
# to rotate the characters.
####################################################################
# Function to encrypt a file
####################################################################
Function Encrypt-File($inputfile,$password,$pincode,$outputlocation)
{
<#
.Synopsis
Encrypt-File [[-inputfile] <string>[]] [[-password] <string>[]] [[-pincode] <string>[]] [[-outputlocation] <string>[]]


.Description 
Encrypt-File takes a txt file and then performs a modified Vignere cipher encryption on the text within that file.
The basis of the encryption is that the password you enter in is converted to a SHA256 HASH. That hash is used as
the encryption key for the plain text. The pin you enter in determines the rotation values to be used in each round
of text transposistion. For every digit you enter with your pin, the text will be encrypted. Example a pin as 324 will
perform 3 rounds of encryption on the text. 

.Example
Encrypt-File -inputfile 'c:\passwords.txt' -password 'P@$$WORD' -pin '19432' -outputlocation 'c:\encryptedfile.txt'
#>



Function Get-StringHash([String] $String,$HashName = "MD5") 
# Thanks for this guy for posting a nice function to get the hash of 
# a string
# https://gallery.technet.microsoft.com/scriptcenter/Get-StringHash-aa843f71
{ 
$StringBuilder = New-Object System.Text.StringBuilder 
[System.Security.Cryptography.HashAlgorithm]::Create($HashName).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($String))|%{ 
[Void]$StringBuilder.Append($_.ToString("x2")) 
} 
$StringBuilder.ToString() 
}

# Now getting the SHA256 hash from the password entered
$SHA2HASH = Get-StringHash -String $password -HashName SHA256

# Now getting the input file that contains sensitive information
$sensitivefile = get-content -Path $inputfile

# Now setting the variables that will be used to run the encryption loops
$encryptedmessage = @()
$hashmover = 0
$class = [System.Text.Encoding]::UTF8
$pinmax = $pincode.Length - 1
###################################################################
# Main Encryption Loop
###################################################################
# This runs a loop for every digit in the pin
foreach ( $p in 0..$pinmax ) { 

#calculating the value to add to the charthashtable
$addvalue = ([int]($pincode[$p].ToString()))

# Checking to see if this is the first initial run and if not then copying the contents from 
# The last execution into the loop input
if ( $encryptedmessage.count -ne 0 ) { $sensitivefile = $encryptedmessage; $encryptedmessage = @() }

# Creating the hashtable chart that contains the values that will be used to encrypt based on the key
$charhash = @{}
foreach ($s in 0..126){
$value = $s+$addvalue
$charhash.Add("$s","$value")
}

#Now running the file through to encrypt the contents of it
foreach ( $i in $sensitivefile ) { 
#converting the text from a line to a char array
$linechar = $i.ToCharArray()
$line = '' 

#Now running each individual char through the encryption process
foreach ( $w in $linechar ) { 
if ($hashmover -eq 64 ) { $hashmover = 0 }
$charlookup = $SHA2HASH[$hashmover] | %{[int]$_}
[int]$charvalue = $charhash."$charlookup"
[int]$encryptedletter = ($w | %{[int]$_}) + $charvalue
if ( $encryptedletter -ge 127 ) { $encryptedletter = ($encryptedletter - 142) + 32 }

# converting the letter from dec to a char and then adding it to a line
[string]$encryptedletter = $class.GetChars($encryptedletter)
$hashmover++
$line = $line+$encryptedletter
}

#adding the line to the message
$encryptedmessage += $line
}

#$encryptedmessage | Set-Content -Path $outputlocation
}
# End of the function
$encryptedmessage | Set-Content -Path $outputlocation
}

####################################################################
# Function to Decrypt a file and open it
####################################################################
Function Decrypt-PasswordVaultFile($inputfile,$password,$pincode) {

<#
.Synopsis
Decrypt-File [[-inputfile] <string>[]] [[-password] <string>[]] [[-pincode] <string>[]]


.Description 
This will decrypt an encrypted password file and then display it in plain text. 

.Example
Decrypt-File -inputfile 'c:\passwords.txt' -password 'P@$$WORD' -pin '19432'

$text = Decrypt-File -inputfile 'c:\passwords.txt' -password 'P@$$WORD' -pin '19432'
#>



Function Get-StringHash([String] $String,$HashName = "MD5") 
# Thank you to this guy for writing a function to get a SHA256 hash from a string
# https://gallery.technet.microsoft.com/scriptcenter/Get-StringHash-aa843f71
{ 
$StringBuilder = New-Object System.Text.StringBuilder 
[System.Security.Cryptography.HashAlgorithm]::Create($HashName).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($String))|%{ 
[Void]$StringBuilder.Append($_.ToString("x2")) 
} 
$StringBuilder.ToString() 
}

# Now setting the hash that will be used as the encryption key
$SHA2HASH = Get-StringHash -String $password -HashName SHA256

#PINCODE
$pinmax = $pincode.Length - 1

# Now getting the input file that contains sensitive information
$sensitivefile = get-content -Path $inputfile

# Now encrypting the sensitive file with the key
$decryptedmessage = @()
$hashmover = 0
$class = [System.Text.Encoding]::UTF8

foreach ( $p in $pinmax..0 ) { 
$addvalue = ([int]($pincode[$p].ToString()))
if ( $decryptedmessage.count -ne 0 ) { $sensitivefile = $decryptedmessage; $decryptedmessage = @()  }
$charhash = @{}
foreach ($s in 0..126){
$value = $s+$addvalue
$charhash.Add("$s","$value")
}

foreach ( $i in $sensitivefile ) { 
# sending the line to a chararray 
$linechar = $i.ToCharArray()
$line = '' 

foreach ( $w in $linechar ) { 
if ($hashmover -eq 64 ) { $hashmover = 0 }
$charlookup = $SHA2HASH[$hashmover] | %{[int]$_}
[int]$charvalue = $charhash."$charlookup"
[int]$encryptedletter = (((($w | %{[int]$_}) - 32) + 142 ) - $charvalue )
if ( $encryptedletter -ge 127 ) { $encryptedletter = ($w | %{[int]$_}) - $charvalue  }
[string]$decryptedletter = $class.GetChars($encryptedletter)  
$hashmover++
$line = $line+$decryptedletter
}
$decryptedmessage += $line
}
}
return $decryptedmessage
}

####################################################################
# Function to add an encrypted password to a file 
####################################################################
Function Insert-EncryptedPassword($inputfile,$password,$pincode,$account,$accountpassword,$accountdescription){

#Decrypt the file in PT
$file = Decrypt-PasswordVaultFile -inputfile $inputfile -password $password -pincode $pincode

# here is where we check to see if the hash checks out
$hash = Get-StringHash -String $file[0] -HashName SHA512
if ( $hash -ne $file[1] ) {write-host "You did not enter the correct password for this vault" } else {

# Add the new line in the file
$line = ($account+'     '+$accountpassword+'     '+$accountdescription)
$file = $file+$line

#

# Now performing the encryption on the file
$SHA2HASH = Get-StringHash -String $password -HashName SHA256

# Now getting the input file that contains sensitive information
$sensitivefile = $file

# Now setting the variables that will be used to run the encryption loops
$encryptedmessage = @()
$hashmover = 0
$class = [System.Text.Encoding]::UTF8
$pinmax = $pincode.Length - 1
###################################################################
# Main Encryption Loop
###################################################################
# This runs a loop for every digit in the pin
foreach ( $p in 0..$pinmax ) { 

#calculating the value to add to the charthashtable
$addvalue = ([int]($pincode[$p].ToString()))

# Checking to see if this is the first initial run and if not then copying the contents from 
# The last execution into the loop input
if ( $encryptedmessage.count -ne 0 ) { $sensitivefile = $encryptedmessage; $encryptedmessage = @() }

# Creating the hashtable chart that contains the values that will be used to encrypt based on the key
$charhash = @{}
foreach ($s in 0..126){
$value = $s+$addvalue
$charhash.Add("$s","$value")
}

#Now running the file through to encrypt the contents of it
foreach ( $i in $sensitivefile ) { 
#converting the text from a line to a char array
$linechar = $i.ToCharArray()
$line = '' 

#Now running each individual char through the encryption process
foreach ( $w in $linechar ) { 
if ($hashmover -eq 64 ) { $hashmover = 0 }
$charlookup = $SHA2HASH[$hashmover] | %{[int]$_}
[int]$charvalue = $charhash."$charlookup"
[int]$encryptedletter = ($w | %{[int]$_}) + $charvalue
if ( $encryptedletter -ge 127 ) { $encryptedletter = ($encryptedletter - 142) + 32 }

# converting the letter from dec to a char and then adding it to a line
[string]$encryptedletter = $class.GetChars($encryptedletter)
$hashmover++
$line = $line+$encryptedletter
}

#adding the line to the message
$encryptedmessage += $line
}

#$encryptedmessage | Set-Content -Path $outputlocation
}
# End of the function
$encryptedmessage | Set-Content -Path $inputfile
write-host "The $account has been added into the vault"
}
}

####################################################################
# Generate a password valut text file 
####################################################################

Function Generate-PasswordVaultFile($path,$description,$password,$pincode)
{ 
$r1 = get-random -Minimum 1000000000000000 -Maximum 9999999999999999
$r2 = get-random -Minimum 1000000000000000 -Maximum 9999999999999999 
$line1 = '###'+(($r1.ToString())+'###>>>>    '+$description+'    <<<<###'+($r2.ToString()))+'###'
$line2 = Get-StringHash -String $line1 -HashName SHA512
$line3 = ''
$file =  @()
$file += $line1
$file += $line2
$file += $line3
$sensitivefile = $file

# Now getting the SHA256 hash from the password entered
$SHA2HASH = Get-StringHash -String $password -HashName SHA256

$encryptedmessage = @()
$hashmover = 0
$class = [System.Text.Encoding]::UTF8
$pinmax = $pincode.Length - 1
###################################################################
# Main Encryption Loop
###################################################################
# This runs a loop for every digit in the pin
foreach ( $p in 0..$pinmax ) { 
#calculating the value to add to the charthashtable
$addvalue = ([int]($pincode[$p].ToString()))
# Checking to see if this is the first initial run and if not then copying the contents from 
# The last execution into the loop input
if ( $encryptedmessage.count -ne 0 ) { $sensitivefile = $encryptedmessage; $encryptedmessage = @() }
# Creating the hashtable chart that contains the values that will be used to encrypt based on the key
$charhash = @{}
foreach ($s in 0..126){
$value = $s+$addvalue
$charhash.Add("$s","$value")
}
#Now running the file through to encrypt the contents of it
foreach ( $i in $sensitivefile ) { 
#converting the text from a line to a char array
$linechar = $i.ToCharArray()
$line = '' 
#Now running each individual char through the encryption process
foreach ( $w in $linechar ) { 
if ($hashmover -eq 64 ) { $hashmover = 0 }
$charlookup = $SHA2HASH[$hashmover] | %{[int]$_}
[int]$charvalue = $charhash."$charlookup"
[int]$encryptedletter = ($w | %{[int]$_}) + $charvalue
if ( $encryptedletter -ge 127 ) { $encryptedletter = ($encryptedletter - 142) + 32 }
# converting the letter from dec to a char and then adding it to a line
[string]$encryptedletter = $class.GetChars($encryptedletter)
$hashmover++
$line = $line+$encryptedletter
}
#adding the line to the message
$encryptedmessage += $line
}
#$encryptedmessage | Set-Content -Path $outputlocation
}
# End of the function
$encryptedmessage | Set-Content -Path $path
}

####################################################################
# HASH FUNCTION
# https://gallery.technet.microsoft.com/scriptcenter/Get-StringHash-aa843f71
####################################################################
Function Get-StringHash([String] $String,$HashName = "MD5") 
{ 
$StringBuilder = New-Object System.Text.StringBuilder 
[System.Security.Cryptography.HashAlgorithm]::Create($HashName).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($String))|%{ 
[Void]$StringBuilder.Append($_.ToString("x2")) 
} 
$StringBuilder.ToString() 
}


