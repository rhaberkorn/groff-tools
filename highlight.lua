#!/usr/local/bin/lua52
local pipe
local line_prefix = ''

for line in io.input():lines() do
	if pipe then
		if line:match("^%. *HIGHLIGHT *") then
			pipe:close()
			pipe = nil
			-- empty line to fix up line numbering
			-- FIXME: the linefeed is necessary because source-highlight did not
			-- terminate the last line
			print "\n."
		else
			-- the last linefeed is not piped, so that we don't get empty lines
			-- at the end of a code block
			pipe:write(line_prefix, line)
			line_prefix = '\n'
		end
	else
		local lang = line:match("^%. *HIGHLIGHT +(.*)$")
		if lang then
			if lang:match(" ") then
				local file
				lang, file = lang:match("^([^ ]*) +(.*)$")
				lang = lang == "default" and "--failsafe" or "-s "..lang
				os.execute("source-highlight --outlang-def groff.outlang "..lang.." -i "..file)
				-- FIXME: Emit .lf statement
				-- FIXME: Omit the last character
				print ""
			else
				lang = lang == "default" and "--failsafe" or "-s "..lang
				pipe = io.popen("source-highlight --outlang-def groff.outlang "..lang, "w")
				-- empty line to fix up line numbering
				print "."
				-- omit linefeed on first print
				line_prefix = ''
			end
		else
			print(line)
		end
	end
end
