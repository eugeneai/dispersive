(setq executable_name "icc_rake_app.py")
(setq project_dir "/home/eugeneai/Development/codes/dispersive/src/icc")
(setq main_executable (concat project_dir "/" executable_name))
; (message main_executable)
(defun run-main-app-shell ()
  (interactive)
  (start-file-process-shell-command "rake_app" "*rake_output*" main_executable))

(setq main-buffer nil)

(defun run-main-app ()
  (interactive)
  (if main-buffer (kill-buffer main-buffer))
  (setq main-buffer (run-python))
  (python-execute-file  (python-proc) main_executable) 
  )

(global-set-key  (kbd "<f5>") 'run-main-app)
;(run-main-app)

(message main_executable)
(message "Loaded environment for RAKE.")
